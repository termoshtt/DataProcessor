Tutorial (Linux/OS X)
====================

Install
-------

ダウンロードして依存関係のパッケージをインストールしてパスを通します。
以下ではホーム(`$HOME`)にインストールしますが、
環境に応じて変更してください。

```command
cd ~
git clone https://github.com/kenbeese/DataProcessor.git
cd DataProcessor
pip install -r requirements.txt # 依存関係のinstall
```

`~/.bashrc`の最後に以下の行を追加してパスを通します。
zsh等を使用している場合は`~/.zshrc`等に読みかえて下さい。

```bash
export PATH=$PATH:$HOME/DataProcessor/bin
export PATH=$PATH:$HOME/DataProcessor/server
export PYTHONPATH=$PYTHONPATH:$HOME/DataProcessor/lib
```

zshを使用している場合は各種コマンドの補完を有効にするため以下を設定します。

```zsh
export FPATH=$FPATH:$HOME/DataProcessor/zsh_completion
```

さらにDataProcessorの設定ファイル`~/.dataprocessor.ini`を生成します。

```command
dpinit
```

を起動すると、
DataProcessorのホームディレクトリと、計算の情報を保持するJSONファイルのパスを聞かれます。
これに答えればインストールは完了です。

単純な使い方(webapp, dpstart)
--------------------------
### webapp (dpserver)

GUIはWEBアプリとして実装してあります。
準備としてBootstrap等のライブラリをダウンロードします。

```command
dpserver install
```

サーバープロセスは以下のコマンドで起動します：

```command
dpserver start
```

特に指定しない場合、8080番のportを使用します。
[http://localhost:8080/](http://localhost:8080/)を開けばプロジェクトの一覧が表示され、
その名前をクリックすると計算の一覧が表示されます。
コメント欄をクリックすればコメントが記入でき、
各プロジェクトのタグの欄の"+"によってタグを作成する事ができます

サーバーを終了するには

```command
dpserver stop
```

とします。

### 計算の開始 (dpstart)
`dpstart`を使用すれば計算の開始と同時に計算をDataProcessorの管理下に置けます。
このスクリプトは以下の動作を行います：

1. 前処理(gitのhash値の取得等)
2. 計算結果を保存するディレクトリを生成
3. 必要なものをそこへコピー
4. 計算を同期/非同期に実行
5. DataProcessorの管理下にこの計算を追加

```
dpstart touch testfile
```

とすれば現在の時刻の名前のディレクトリがインストール時に設定した`root`以下の
`Runs`以下に生成され、その中に`testfile`が`touch`コマンドにより作成されます。

この動作を制御するため、`dpstart`は多くのオプションを取ります。

- require : 必要なものを追加します
- runner : どうやって計算を実行するか決めます
    - sync: 終了を待ちます(同期)
    - daemon: デーモンプロセスとして計算を開始します(非同期)
    - atnow: (for Linux) atdを使用します(非同期)

複雑な使い方(dpmanip)
---------------------

CUIによるメタデータの操作は実行可能スクリプト`dpmanip`を通して行います。
このコマンドは以下の様に、多くのサブコマンドを持っています。

### 新しい計算の追加
[`add_run`を使用する場合](#add_runを使用する場合)に書いてある通り、

```command
dpmanip add_run /path/to/run --tag tagname --comment "comment comment"
```

で追加できます。

### コメント追加

計算にコメントを追加するには[webapp](http://localhost:8080/)を使用する方法と
`dpmanip`を使用する方法があります。
webappではコメント覧をクリックするとコメントが入力できます。
フォーカスが外れると変更が保存されます。

`dpmanip`は以下の様にして使います：

```command
dpmanip add_comment "comment" /path/of/run
```

`"comment"`にはコメントしたい文字列を、
`/path/of/run`にはコメントしたい計算のpathを入力します。
現在のディレクトリの計算にコメントを付けるには

```command
dpmanip add_comment "comment" .
```

とします。

### タグの追加と取り外し

計算にタグを付ける事ができます。
タグは内部的にはプロジェクトと同じなので、
webappのプロジェクトのリストにタグも一緒に一覧されます。

```command
dpmanip add_tag /path/of/run "tagname"
```

`"tagname"`の替りに存在しているプロジェクトのパスを書く事もできます。

```command
dpmanip add_tag /path/of/run /path/of/project
```

tagは以下のコマンドで外せます。

```command
dpmanip untag /path/of/run tagname
```

or

```command
dpmanip untag /path/of/run /path/of/project
```

### 既存の計算のスキャン

おそらくあなたは既に多くの計算を実行し、
独自の方法でその管理を行なっているでしょう。
ここではそれらの計算をDataProcessorで管理する準備をします。

以下で2通りの方法を説明します。

#### `scan_directory`を使用する場合
この作業は以下の事を仮定します。
- 計算とディレクトリが一対一対応している
- そのディレクトリに特定の名前のファイルがある

この条件を満している場合は`scan_directory`を使用する事ができます。

```command
dpmanip scan_directory /path/of/root/directory "*.ini"
```

`/path/of/root/directory`は計算に対応するディレクトリの親ディレクトリを指定します。
このディレクトリ以下を再帰的にスキャンして管理下に置きます。
もし複数に分れている時は複数回呼びます。

```command
dpmanip scan_directory /main/path/of/root/directory "*.ini"
dpmanip scan_directory /another/path/of/directory "*.ini"
```

最後の引数`"*.ini"`は見つけたディレクトリが計算と
対応しているディレクトリがどうかを判定するために使います。
もし`"*.ini"`に一致するファイルがある場合はそのディレクトリを
計算に対応しているディレクトリとして扱います。

#### `add_run`を使用する場合

上記の条件を満たしていない場合、各ランのディレクトリを個別に登録します。

```command
dpmanip add_run /path/to/run
```

で登録できます。

同時にtag、commentや別名を残したい場合は

```command
dpmanip add_run /path/to/run --tag tagname_or_projectpath --name run_run_run --comment "The best run."
```

で出来ます。tagやcommentは後からでも下に記述してあるように、
`add_tag`, `add_comment`で追加できます。


### 計算のパラメータの読み込む
上述の作業ではまだ計算とディレクトリを対応させただけです。
次に個々の計算のパラメータを登録します。


#### 方法1

もし計算のディレクトリに設定ファイルがINI形式で保存されていれば
```command
dpmanip configure conf.ini
```

`conf.ini`はINIファイルの名前に変更してください。

拡張子が異なる場合は指定することができます。
```command
dpmanip configure conf.conf ini
```

セクションのないINIファイル

```
A = 1
B = 1.0
C = 2.0
```

のような場合には

```command
dpmanip configure_no_section conf.ini
```

で可能です。

#### 方法2
設定ファイルが独自形式の場合、各ランのパラメータを

```command
dpmanip add_conf /path/to/run a 1
dpmanip add_conf /path/to/run b 1.0
dpmanip add_conf /path/to/run c 2.0
```

で登録可能です。
