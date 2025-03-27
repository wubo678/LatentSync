
# 🎙️ LatentSync

## 🔥 更新日志

- **2025/03/14**：发布 **LatentSync 1.5**：
  1. 通过引入时序层改进了时序一致性；
  2. 对中文视频表现更好；
  3. 经过优化后，第 2 阶段训练所需显存降低为 **20GB**。

详细更新见：[changelog_v1.5](docs/changelog_v1.5.md)

## 📖 简介

**LatentSync** 是一种端到端的音频驱动口型同步方法，基于 latent diffusion 模型。不同于传统的像素空间扩散或两阶段生成，LatentSync **无需中间动作表示**，直接建模音视频之间的复杂关联，利用了 Stable Diffusion 的强大建模能力。

## 🏗️ 模型框架

LatentSync 使用 [Whisper](https://github.com/openai/whisper) 将 melspectrogram 转换为音频嵌入，并通过 cross-attention 融入 U-Net。参考帧与遮罩帧与加噪 latent 拼接后作为 U-Net 输入。

训练中，模型使用一步去噪恢复干净 latent，再解码得到清晰帧。损失函数包括像素空间的 TREPA、[LPIPS](https://arxiv.org/abs/1801.03924)、[SyncNet](https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf)。

## 🎬 演示视频

左侧为原始视频，右侧为生成的同步口型视频（照片级真实视频由模特拍摄，动漫视频来自 [VASA-1](https://www.microsoft.com/en-us/research/project/vasa-1/) 和 [EMO](https://humanaigc.github.io/emote-portrait-alive/)）。

## 📑 开源内容

- ✅ 推理代码和模型权重  
- ✅ 数据处理流程  
- ✅ 训练代码  

## 🔧 环境配置

一键安装依赖并下载模型：
```bash
source setup_env.sh
```

下载完成后，`checkpoints/` 文件夹中应包含：
```
latentsync_unet.pt
stable_syncnet.pt
whisper/tiny.pt
auxiliary/ 各类辅助模型
```

> 如果你只想运行推理，只需下载 `latentsync_unet.pt` 和 `tiny.pt`。

## 🚀 推理方式（需要 6.8 GB 显存）

### 1. 使用 Gradio Web 应用

```bash
python gradio_app.py
```

### 2. 使用命令行接口

```bash
./inference.sh
```

可调参数：
- `inference_steps`：影响画质（20-50），越大越精细；
- `guidance_scale`：影响口型准确性（1.0-3.0），越大越精确，但可能带来失真。

## 🔄 数据处理流程

完整流程如下：

1. 删除损坏视频；
2. 视频帧率重采样为 25FPS，音频重采样为 16000Hz；
3. 使用 [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) 进行镜头检测；
4. 每段视频切分为 5-10 秒；
5. 使用 [face-alignment](https://github.com/1adrianb/face-alignment) 检测关键点，对人脸进行仿射变换；
6. 移除同步得分低于 3 的视频；
7. 计算 [HyperIQA](https://openaccess.thecvf.com/content_CVPR_2020/papers/Su_Blindly_Assess_Image_Quality_in_the_Wild_Guided_by_a_CVPR_2020_paper.pdf) 图像质量分，移除得分低于 40 的视频。

运行处理脚本：
```bash
./data_processing_pipeline.sh
```

输出将保存在 `high_visual_quality/` 目录中。

## 🏋️‍♂️ 训练 U-Net

训练前请完成数据处理并下载所有模型权重。我们提供了在 VoxCeleb2 和 HDTF 上达到 94% 准确率的预训练 SyncNet 模型用于监督。

执行训练：
```bash
./train_unet.sh
```

配置文件位于 `configs/unet`：

| 配置文件 | 显存需求 | 说明 |
|----------|----------|------|
| `stage1.yaml` | **23 GB** | 第一阶段训练 |
| `stage2.yaml` | **30 GB** | 完整精度训练 |
| `stage2_efficient.yaml` | **20 GB** | 效率优化版，适合 RTX 3090，画质稍弱 |

使用前请根据你的数据路径修改配置。

生成文件列表：
```bash
python -m tools.write_fileslist
```

## 🧠 训练 SyncNet

如果你要在自定义数据上训练 SyncNet，执行：
```bash
./train_syncnet.sh
```

训练过程会生成损失曲线图（训练 & 验证），保存在 `train_output_dir`。

要自定义网络结构，请参考：[docs/syncnet_arch.md](docs/syncnet_arch.md)

## 📊 模型评估

### 评估视频同步得分：
```bash
./eval/eval_sync_conf.sh
```

### 评估 SyncNet 准确率：
```bash
./eval/eval_syncnet_acc.sh
```

⚠ 注意：评估前，**测试数据也必须先经过数据处理流程**，否则 SyncNet 可能失效。

## 🙏 鸣谢

本项目基于以下开源项目构建：

- [AnimateDiff](https://github.com/guoyww/AnimateDiff)  
- [MuseTalk](https://github.com/TMElyralab/MuseTalk)  
- [StyleSync](https://github.com/guanjz20/StyleSync)  
- [SyncNet](https://github.com/joonson/syncnet_python)  
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip)

感谢这些项目的开源支持 ❤️

## 📖 引用方式

如果你在研究中使用了 LatentSync，请引用以下论文：

```bibtex
@article{li2024latentsync,
  title={LatentSync: Taming Audio-Conditioned Latent Diffusion Models for Lip Sync with SyncNet Supervision},
  author={Li, Chunyu and Zhang, Chao and ...},
  journal={arXiv preprint arXiv:2412.09262},
  year={2024}
}
```
