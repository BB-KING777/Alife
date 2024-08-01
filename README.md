このリポジトリでは、O'REILLY　ジャパンの「作って動かすAlife」をもとにして、Alifeの勉強をしています。

# チャプター2
## グレイスコットモデル
自然界に存在する様々なパターンは「'化学反応と拡散過程'」という自己組織的なロジックで作成できる。
どのようにしてその生態系を作るのかを表す方程式「'反応拡散系'(モルフォゲン方程式)」。

### グレイスコット方程式
$$
\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + F(1 - u)
$$
$$
\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (F + k)v
$$

$u$と$v$はそれぞれ、反応物Aと反応物によって生成される物質Bの濃度を表す
$D_u$と$D_v$は$u$と$v$の拡散係数
$F$は供給率で外部からの$u$の供給と反応のバランスを表す
$k$は消失率で$v$の消失を表す

$\nabla^2$はラプラシアン演算子で物質の空間的な拡散を表すことができる
$-uv^2$はuとvの非線形反応項で特定の条件下での自発的なパターン形成を引き起こす
$F(1-u)$は供給項で外部からuを供給する
$-(F+k)v$は消失項であり、$v$が全体から消失する速度を表す

#### ラプラシアン
2次元空間でのスカラー場$\phi$を表すラプラシアンは
$$
\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2}
$$
となる。$\phi$の二階偏微分のそれぞれの和である。


スカラー場もしくはベクトル場の各点における変化の度合いを記述する


$$\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + F(1 - u)$$
と
$$\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (F + k)v$$
#### 解説

$$\frac{\partial u}{\partial t}$$
および
$$\frac{\partial v}{\partial t}$$
はΔtにおける物質uと物質vの**濃度**の変化量を表す。

$$D_u \nabla^2 u$$
$$D_v \nabla^2 v$$
はそれぞれ、$D_u$と$D_v$は拡散係数である。

$\nabla^2 u$と$\nabla^2 v$はそれぞれ、$u$と$v$の各方向(2次元の場合x,y)における拡散度合いを示す。そのため、これに拡散係数$D_u$ $D_v$をかけることによって拡散度合いが変化する

$$-uv^2$$
$$+uv^2$$
では上の式は、uが$v^2$と反応してuが消費される速度を表す。

下の式では、vがuと反応してvが生成されるのを表す。



$$F(1-u)$$は、uの供給項である。つまり、uの発生源である。Fはuがどれだけ発生するかを表す。また、(1-u)では、uの量が1に近ければ発生し、1に遠ければ発生しない。

$$-(F+k)v$$
では、Fは反応系の消失率を表す。kはvが全体から消失する速度を決定する。

## ライフゲーム
ライフゲームとは、イギリスのジョン・コンウェイが提案した二次元セルラーオートマトンのルールセットである。セルラーオートマトンは非線形であり、実行してみないとわからない。

オートマトンになじみない人のために、通常のオートマトンについても記述する

### オートマトン
オートマトンとは、計算および処理を行うための抽象的な機械やシステムを指す。オートマントは入力を受けとり、それに基づいて状態を遷移して最終的に出力を生成するモデルである。日本語では「**状態機械**」という素晴らしい訳がある。



	50円の硬貨のみを受け付ける自動販売機
	150になると飲み物を出力する

これを考える。
一つ目の状態遷移を考えると、0円に対して50円になるため状態が遷移する。

![[Pasted image 20240801015138.png]]

こういった状態遷移が考えられる。これらを示すのがオートマトン/状態機械である。


### セルラーオートマトン
セルラーオートマトンにはルールセットがあると先ほど述べた。そのように、セルラーオートマトンにはいくつかのルールの種類があり、それぞれ細かくルールが違う。下記のルールはすべてのルールで適応できるものである。

	空間がある:2次元の場合オセロの盤面のようなセルがある
	時間がある:セルの状態が変化するための時間ステップがある
	セルに状態がある:簡単な例は死;生などである
	セルの状態が変わる条件がある:餓死などが例である。ここでは、左右上下のセルの状態によって判断する


#### 一次元でのセルラーオートマトン

![[Pasted image 20240801015921.png]]
このセルを考える。

これは一次元セルラーオートマトンと呼ばれるもので、ルールは以下のようなものがある。

	空間が一次元
	時間は一斉更新
	状態は2パターン、生か死か
	状態遷移条件は256通り

状態更新条件の計算方法
3つのセルがあり、それぞれ2つの通り数を持つことが可能なので、
$$2^3$$
である。また、これらの並び替えを考えると

$$2^8$$
と考えられるよって256通りである。

![[Pasted image 20240801102028.png]]

これらを用いてルールを決定する。上記の並び方ではルールは、22ということになる。

上の3つのセルの配置の時、一つ下のセルは画像の下のように変化するということである。

これらのルールを適応したセルラーオートマトンを動かすと以下のようなクラスに分類できる

#### クラス1

時間的にパターンが消えたり、固定化するもの

例:ルール40 232

#### クラス2
周期的な構造を作るようになり、無限にそのパターンを繰り返す

例:ルール94 108

#### クラス3
非周期でランダムなカオスを作り出す

例:ルール54 90

#### クラス4
時間的空間的に局在する構造を持つ複雑なパターンを作り出す

例:ルール110 121

### 二次元セルラーオートマトン

先ほどの一次元では、両隣のみからの影響を受けたが、2次元では上下左右斜めからも影響を受ける。

ルールは以下である。

	人口過剰:生きているセルが、囲まれているセル3つより多くのセルが生きていればそのセルは死ぬ

	均衡状態:生きているセルの囲んでいるセルのうち2つor3つが生きていればそのセルは生き残る

	人口過疎:生きているセルの囲んでいるセルのうち、2つ未満のセルしか生きていない場合、そのセルは死ぬ

	再生:死んでいるセルが、囲まれているセルのちょうど3つが生きていればそのセルは生き返る。


これらには以下のパターンが存在する

1.ランダムパターン:ランダムなパターン
2.静的パターン:静的なパターン
3.オシレーター:いくつかのステップ後に初期状態に戻るもの
4.グライダー:あるパターンが壊れることなくセルを移動するもの
5.グライダーガン:グライダーがグライダーを作り出し、周囲に送るもの
