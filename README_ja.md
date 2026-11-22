# Video Scene Extractor

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

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

- [uv](https://docs.astral.sh/uv/)（推奨）、または uv を使わない場合は Python 3.10 以上
- `PATH` から実行できる FFmpeg

FFmpeg は各 OS のパッケージ管理方法でインストールしてください。Windows ネイティブでは Windows 用の FFmpeg を導入し、`ffmpeg.exe` を Windows の `PATH` に追加してください。WSL 内の FFmpeg とは別に設定が必要です。

### プロジェクトのインストール

リポジトリを取得し、プロジェクトディレクトリで環境を同期します。WSL と Windows ネイティブ（PowerShell）のどちらでも同じコマンドを使えます。

```sh
git clone https://github.com/yourusername/video-scene-extractor.git
cd video-scene-extractor
uv sync
```

`.venv` が作成され、プロジェクト本体・依存関係・`dev` グループの開発ツールがインストールされます。WSL と Windows ネイティブで仮想環境を共有せず、それぞれの環境で `uv sync` を実行してください。

同じ Windows 上のチェックアウトを WSL と Windows の両方から使う場合、WSL ではラッパー（`.venv-wsl` を選択）を使ってください。直接 uv を実行する場合は、先に次を設定します。

```bash
export UV_PROJECT_ENVIRONMENT="$PWD/.venv-wsl"
```

### 同じチェックアウトを Windows と WSL から使う場合

Python の仮想環境は OS ごとに異なります。同じ Windows ファイルシステム上のチェックアウトを共有している場合でも、Windows ネイティブと WSL で 1 つの `.venv` を共用しないでください。Windows ネイティブでは `.venv`、WSL では `.venv-wsl` を使用します。

両方の環境で `.venv` を使うと、`uv` が別のプラットフォームで作成された仮想環境を検出することがあります。実行するコマンド、uv のバージョン、実行側のプラットフォームによっては、uv が仮想環境を再作成する場合もあれば、置き換えずにエラーで停止する場合もあります。その結果、もう一方の環境から次に起動したときに失敗することがあります。

この問題を避けるには、付属のラッパーを使用してください。`video-scene-extractor.ps1` は Windows で `.venv` を使用し、`video-scene-extractor.sh` は WSL で実行すると `.venv-wsl` を使用します。WSL で `uv` を直接実行する場合は、上記のとおり `UV_PROJECT_ENVIRONMENT` を設定してください。直接 `uv` を使うことが多い場合は、この変数を WSL のシェル設定に追加してください。

互換性のない仮想環境から復旧するには、現在使用している OS 側の仮想環境だけを削除してから、uv に再作成させます。

**Windows PowerShell:**

```powershell
Remove-Item -Recurse -Force .venv
uv sync
```

**WSL:**

```bash
rm -rf .venv-wsl
UV_PROJECT_ENVIRONMENT=.venv-wsl uv sync
```

もう一方の OS 用の仮想環境は、その環境でも再構築する場合以外は削除しないでください。

`uv` を使わない場合は、選択した Python 環境にプロジェクトと依存関係をインストールしてください。

**Windows PowerShell:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

**Linux、macOS:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

**同じ Windows 上のチェックアウトを使う WSL:**

```bash
python3 -m venv .venv-wsl
.venv-wsl/bin/python -m pip install -e .
```

## クイックスタート

OS に合わせたラッパーを使うと、実行環境を自動で選択します。

**Windows PowerShell:**

```powershell
.\video-scene-extractor.ps1 input_video.mp4
```

**Linux、macOS、WSL:**

```bash
bash video-scene-extractor.sh input_video.mp4
```

ラッパーは `uv` を最優先し、次にプロジェクト内の `.venv` または `venv`、最後にローカルの Python 3.10 以上を使います。`uv` を使わない場合、選択された環境に依存関係をあらかじめインストールしてください。WSL では、Windows と同じチェックアウトを使っても Windows 用 `.venv` を共有しないよう、既定で `.venv-wsl` を使います。

CLI は `uv run video-scene-extractor ...` で直接実行することもできます。

これにより：
1. `input_video.mp4` のシーン変化を検出
2. 各シーン変化時点のスクリーンショットを抽出
3. 画像を含む `output.pdf` を作成

### 出力ファイルを指定

```sh
uv run video-scene-extractor input_video.mp4 -o slides.pdf
```

### 検出感度を調整

```sh
# 閾値を高くすると大きな変化のみ検出（スライド向け）
uv run video-scene-extractor input_video.mp4 -t 25.0

# 閾値を低くすると細かな変化も検出（デモ向け）
uv run video-scene-extractor input_video.mp4 -t 10.0
```

### 抽出した画像を保持

```sh
uv run video-scene-extractor input_video.mp4 --keep-images --output-dir ./frames
```

### ドキュメント用に縦向き PDF を作成

```sh
uv run video-scene-extractor document.mp4 --orientation portrait --title "ドキュメント資料"
```

### Ruff チェック

```sh
uv run ruff check .
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


---

