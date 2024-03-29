"""
基本 Demo
"""
import time

from modelscope import AutoModel, AutoTokenizer, snapshot_download

TOKENIZER = None
MODEL = None


def init_model():
    """
    初始化 ChatGLM3 模型
    """
    global TOKENIZER, MODEL  # pylint: disable=W0603

    # Download models: https://modelscope.cn/models/ZhipuAI/chatglm3-6b/summary
    # model_dir: str = snapshot_download(
    #     "ZhipuAI/chatglm3-6b", revision="master", cache_dir=model_path, local_files_only=True
    # )

    # Model path on Windows: C:\Users\<UserName>\.cache\modelscope\hub
    model_dir: str = snapshot_download("ZhipuAI/chatglm3-6b", revision="master", local_files_only=True)

    if TOKENIZER is None:
        TOKENIZER = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

    if MODEL is None:
        # GPU 推理，默认 FP16 精度加载，需要 13GB 显存
        # MODEL = AutoModel.from_pretrained(model_dir, trust_remote_code=True).cuda()
        # MODEL = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
        # 模型 4-bit 量化，减少显存压力，6GB 显存即可
        MODEL = AutoModel.from_pretrained(model_dir, trust_remote_code=True).quantize(4).cuda()
        # CPU 推理，要求 32GB 内存空间
        # MODEL = AutoModel.from_pretrained(model_dir, trust_remote_code=True).float()
        MODEL = MODEL.eval()


def chat(content: str, chat_history: list):
    """
    对话
    """
    if (MODEL is None) or (TOKENIZER is None):
        raise RuntimeError("模型未初始化！")

    t: float = time.perf_counter()
    print(f"用户：{content}")
    response, _history = MODEL.chat(TOKENIZER, content, history=chat_history)
    print(f"ChatGLM3-6B：{response}")
    print(f"花费时间：{(time.perf_counter() - t):.2f}秒\n")
    return _history


if __name__ == "__main__":
    init_model()

    history = chat("你好！", [])
    history = chat("圣诞节是什么时候？", history)
