# Video Scene Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

研修動画やプレゼンテーション動画から、シーン変化を検出して重要な場面のスクリーンショットを自動抽出し、PDFにまとめるツールです。

[English README is here](README.md)

## 特徴

- 🎬 **自動シーン検出**: PySceneDetectを使用して動画のシーン変化を自動検出
- 📸 **スマート抽出**: 大きな変化があった場面のみを抽出
- 📄 **PDF生成**: 抽出した画像を1つのPDFドキュメントに統合
- ⚙️ **高度な設定**: 閾値や品質など柔軟な設定が可能
- 🖥️ **クロスプラットフォーム**: Windows (WSL)、macOS、Linuxで動作
- 🚀 **CLIインターフェース**: 使いやすいコマンドラインツール

## 用途

- プレゼンテーション動画からスライドを抽出
- デモ動画から画面遷移をキャプチャ
- 研修動画のサマリーを作成
- 動画コンテンツをPDFとして記録

## インストール

### 前提条件

- Python 3.8以上
- FFmpeg

#### FFmpegのインストール

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows (WSL):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### インストール

#### 方法1: セットアップスクリプトを使用（推奨）

```bash
git clone https://github.com/yourusername/video-scene-extractor.git
cd video-scene-extractor
./setup.sh
```

セットアップスクリプトは以下を自動的に実行します：
- Python仮想環境の作成
- 依存関係のインストール
- パッケージのインストール

#### 方法2: 手動インストール

```bash
git clone https://github.com/yourusername/video-scene-extractor.git
cd video-scene-extractor
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
pip install -e .
```

## クイックスタート

### 基本的な使い方

#### ラッパースクリプトを使用（推奨）

動画からスクリーンショットを抽出してPDFを作成：

```bash
./video-scene-extractor.sh input_video.mp4
```

#### 仮想環境を手動でアクティベート

```bash
source venv/bin/activate
video-scene-extractor input_video.mp4
```

**注意**: ラッパースクリプト（`video-scene-extractor.sh`）を使用すると、仮想環境の管理が自動化されます。

これにより：
1. `input_video.mp4`のシーン変化を検出
2. 各シーン変化時点でスクリーンショットを抽出
3. すべてのスクリーンショットを含む`output.pdf`を作成

### 出力ファイルを指定

```bash
./video-scene-extractor.sh input_video.mp4 -o slides.pdf
```

### 検出感度を調整

```bash
# 閾値を高く = 大きな変化のみ検出（スライド向け）
./video-scene-extractor.sh input_video.mp4 -t 25.0

# 閾値を低く = より細かい変化も検出（デモ向け）
./video-scene-extractor.sh input_video.mp4 -t 10.0
```

### 抽出した画像を保持

```bash
./video-scene-extractor.sh input_video.mp4 --keep-images --output-dir ./frames
```

### ドキュメント用に縦向きPDF

```bash
./video-scene-extractor.sh document.mp4 --orientation portrait --title "ドキュメント資料"
```

## コマンドラインオプション

```
Usage: video-scene-extractor [OPTIONS] INPUT_VIDEO

Arguments:
  INPUT_VIDEO              Input video file path

Output Options:
  -o, --output PATH        Output PDF file path [default: output.pdf]
  --output-dir PATH        Image output directory [default: ./frames]
  --keep-images            Keep images after PDF generation

Scene Detection Options:
  -t, --threshold FLOAT    Scene detection threshold (0-100) [default: 17.0]
  --min-scene-len INT      Minimum scene length in frames [default: 15]
  --position TEXT          Frame extraction position (start/middle/end) [default: start]

Image Options:
  --format TEXT            Image format (jpg/png) [default: jpg]
  --quality INT            JPEG quality (1-100) [default: 95]
  --max-width INT          Maximum width in pixels
  --max-height INT         Maximum height in pixels

PDF Options:
  --page-size TEXT         Page size (A4/Letter) [default: A4]
  --orientation TEXT       Page orientation (portrait/landscape) [default: portrait]
  --no-timestamp           Hide timestamp on images
  --title TEXT             PDF title

Other Options:
  --config PATH            Configuration file path
  --verbose, -v            Verbose output
  --version                Show version
  --help                   Show help message
```

## 設定ファイル

YAML形式の設定ファイルで永続的な設定が可能です。複数回の実行で一貫した設定を維持するのに便利です。

### 設定ファイルの作成

1. テンプレートファイルをコピー：
```bash
cp config.yaml.template config.yaml
```

2. `config.yaml`を編集して好みの設定を記述：
```yaml
# config.yaml
detection:
  threshold: 17.0        # シーン検出の感度
  min_scene_len: 15      # 最小シーン長（フレーム数）
  position: start        # フレーム抽出位置（start/middle/end）

image:
  format: jpg            # 画像形式（jpg/png）
  quality: 95            # JPEG品質（1-100）
  max_width: 1920        # 最大幅（null = 元のサイズを維持）
  max_height: 1080       # 最大高さ（null = 元のサイズを維持）

pdf:
  page_size: A4          # ページサイズ（A4/Letter/A3/Legal）
  orientation: landscape # ページ向き（portrait/landscape）
  add_timestamp: true    # 画像にタイムスタンプを追加
  title: null            # PDFタイトル（null = 動画ファイル名を使用）

output:
  output_dir: ./frames   # 抽出画像の保存ディレクトリ
  keep_images: false     # PDF生成後も画像を保持
  verbose: false         # 詳細ログを有効化
```

3. 設定ファイルを使用：
```bash
video-scene-extractor input_video.mp4 --config config.yaml
```

**注意:** `config.yaml`は個人設定を保護するためgit管理対象外です。リポジトリにはテンプレートファイルのみが含まれます。

### 設定例

`examples/`ディレクトリには、一般的な用途向けの事前設定ファイルがあります：

**プレゼンテーションスライド用** (`examples/config_slides.yaml`):
- 高い閾値（20.0）でスライド切替を検出
- PNG形式で高品質
- 横向き

**デモ動画用** (`examples/config_demo.yaml`):
- 低い閾値（12.0）で微細な変化を検出
- JPEG形式でファイルサイズを削減
- 横向き（ワイドスクリーンデモ用）

設定例の使用：
```bash
video-scene-extractor input_video.mp4 --config examples/config_slides.yaml
```

### コマンドライン引数が設定ファイルを上書き

コマンドライン引数は常に設定ファイルの設定より優先されます：
```bash
# config.yamlを使用しつつ、閾値のみ上書き
video-scene-extractor input_video.mp4 --config config.yaml -t 25.0
```

## 閾値調整ガイド

`threshold`パラメータでシーン検出の感度を制御します：

| 動画タイプ | 推奨閾値 | 説明 |
|-----------|---------|------|
| プレゼンテーションスライド | 15-25 | スライド切替を検出 |
| デモ動画 | 10-15 | 画面変化を検出 |
| 混合コンテンツ | 17（デフォルト） | バランスの取れた検出 |
| 微細な変化 | 5-10 | より敏感に検出 |

**ヒント:**
- まずデフォルト値（17.0）から始めて、結果に応じて調整
- 高い値 = より少ない、重要なシーンのみ
- 低い値 = より多くのシーン、微細な変化も含む
- 短い動画クリップでテストしてから本番実行

## 使用例

### 研修動画からスライドを抽出

```bash
video-scene-extractor training.mp4 \
  -o training_slides.pdf \
  -t 20.0 \
  --orientation landscape \
  --title "研修資料"
```

### デモのスクリーンショットをキャプチャ

```bash
video-scene-extractor demo.mp4 \
  -o demo_screenshots.pdf \
  -t 12.0 \
  --keep-images \
  --output-dir ./demo_frames
```

### 高品質PNG出力

```bash
video-scene-extractor presentation.mp4 \
  --format png \
  --quality 100 \
  --max-width 1920 \
  --max-height 1080
```

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) - シーン検出エンジン
- [FFmpeg](https://ffmpeg.org/) - 動画処理
- [Pillow](https://python-pillow.org/) - 画像処理
- [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf) - PDF生成

## トラブルシューティング

### FFmpegが見つからない

```bash
# FFmpegがインストールされているか確認
ffmpeg -version

# インストールされていない場合は、上記のインストール手順を参照
```

### メモリ不足エラー

大容量の動画を処理する場合、以下のオプションを試してください：

```bash
# 画像サイズを制限
video-scene-extractor large_video.mp4 --max-width 1280 --max-height 720

# 閾値を上げて抽出枚数を減らす
video-scene-extractor large_video.mp4 -t 25.0
```

### 抽出枚数が多すぎる/少なすぎる

閾値を調整してください：

```bash
# 枚数が多すぎる場合は閾値を上げる
video-scene-extractor video.mp4 -t 25.0

# 枚数が少なすぎる場合は閾値を下げる
video-scene-extractor video.mp4 -t 10.0
```

## よくある質問

**Q: どのような動画フォーマットに対応していますか？**

A: FFmpegがサポートするすべてのフォーマット（MP4、AVI、MOV、MKVなど）に対応しています。

**Q: 処理時間はどのくらいかかりますか？**

A: 動画の長さと解像度によりますが、1時間の動画で5-10分程度が目安です。

**Q: 商用利用は可能ですか？**

A: はい、MITライセンスの下で商用利用が可能です。

---

