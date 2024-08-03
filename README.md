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


# チャプター3 個と自己複製

## 個と自己複製

ALifeにおいて、個の定義や自己複製はなくてはならないものである。

個を規定するプロセスとは何であろうか？

データベースにおける実体はどのように定義されるか。それは区別可能な存在である。山田太郎や、猫のミケなどである。彼らは、外部に対して壁をもって存在している。それらは細胞である。つまり、個を規定するものは壁(膜)である。壁と書くと壁の内と外では化学物質や情報のやり取りがなくなるので、コロイド膜のような、**情報のやり取りはあるけれど、存在する壁として以後は膜**とかく。

なぜここまで、膜にこだわるのか。これは、膜の内側のみで情報のやり取りが完結してしまえば、それは個ではなくなる。生物は外部の環境とやり取りしながら個を規定している。内部のみで完結してしまえば、外部の世界は不要なのでそれは個ではない。

また、不安定な個、たとえば常に変化するようなカオスな状態、それもまた個ではない。煙や、水が個であるかと言われればそれは個ではない

つまり、個というのは「安定しつつ、不安定なもの」ということである。

私は安定していますが、ということを感じた人は、あなたは体の中で栄養を生み出して外部との接触なしに存在しているかと言われればおそらく、そんなSFチックは人はいないだろう。もしいれば、教えてほしい。

### オートポイエーシス
ここで**オートポエイシース**という概念を説明する。

これは個の創発においてなくてはならないものである。

オートポエイシースとは、**自らを生成し、自らを維持できる最小単位の生命**の機構を持つシステムのことである

#### 余談

ちなみに、これを発明したチリの生物学者ウンベルト・マトゥラーナとフランシスコ・バレーラは、生命の有機機構とは何かを解明するために発案した。

古代から、学者たちは声明を説明するには何が必要かを考察してきた。現代でも魂や精神など非物質的なものがよく説明に用いられるが、そんなことを言い出したら、なんでもOKになるガバガバ説明なため、物質的なものや働きのみから生命の説明を試みる**機械論**が重要である。ウンベルトとバレーラも経験科学者のため、こういった魂だの精神だのの議論には反対の立場である。


	オートポイエティック・マシンとは、構成素が構成素を産出するという産出（変形および破壊）過程のネットワークとして、有機的に構成（単位体として規定）された機械である。このとき構成素は、次のような特徴をもつ。
	（ⅰ）変換と相互作用をつうじて、自己を産出するプロセス（関係）のネットワークを、絶えず再生産し実現する、
	（ⅱ）ネットワーク（機械）を空間に具体的な単位体として構成し、またその空間内において構成素は、ネットワークが実現する位相的 [topological] 領域を特定することによってみずからが存在する。
	―引用元　：H・Rマトゥラーナ&F・Jヴァレラ『オートポイエーシスー生命システムとはなにか』1991、国文社、70-71頁 (Wikipediaより引用)

これらがウルベルトとバレーラが提唱したオートポイエーシスである。

オート・ポイエーシスの語源は、オート(自己)・ポイエーシス(生産)である。つまり、自己創出である。

オートポイエーシスの条件

	1. 生成プロセスは次の生成プロセスへ自動的に接続する
	2. 生成プロセスは要素を産出する
	3. 産出された要素が、1を再度作動させる。生み出された要素がプロセスそのものを作動させる
	4. 生成プロセスの継続が、実行を通じて自動的に閉域を定める
	5. 要素はそれらが存在することによって自らが存在する場所を固有化する。つまり、生成プロセスが特定の空間内に出現する。



## SCLモデル

SCLモデルは、個の創発とは何かという問いに対して以下のように答える
	個の創発とは、自己の存在を決定するのはそれ自体を構成するのプロセスによってである

ということを主張する。

SCLには3つの要素が存在する
1. 基質分子 S
2. 触媒分子 C
3. 膜分子 L

```
2S + C → L + C　　>>> 1

L + L → L - L     >>> 2

L → 2S           >>> 3

```


の化学反応を定義する。

1. 2つの基質分子から触媒Cによって膜分子Lと触媒分子が生成される
2. 2つの隣り合う膜分子は、結合し、空間上に固定される
3. 膜分子は一定の確率で、2つの基質分子に分解される。


![[Pasted image 20240803124027.png]]


以下のコードを実行すると上記の画像のようなものが起動する。これらは、四角が膜分子であり、それらが線としてつながることで明確な壁となり個を形成する。

### コード

```
import sys
import numpy as np
import pygame
import random

# Constants
SPACE_SIZE = 16
CELL_SIZE = 40

# Colors
COLORS = {
    'HOLE': (255, 255, 255),          # White (same as the background)
    'SUBSTRATE': (0, 255, 255),   # Cyan
    'CATALYST': (255, 0, 255),    # Magenta
    'LINK': (0, 0, 255),        # Blue
    'LINK_SUBSTRATE': (255, 255, 0)  # Yellow
}

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SPACE_SIZE * CELL_SIZE, SPACE_SIZE * CELL_SIZE))
pygame.display.set_caption("SCL Simulation")

# Initial configuration
INITIAL_SUBSTRATE_DENSITY = 0.8
INITIAL_CATALYST_POSITIONS = [(8, 8)]

# Model parameters
MOBILITY_FACTOR = {
    'HOLE': 0.1,
    'SUBSTRATE': 0.1,
    'CATALYST': 0.0001,
    'LINK': 0.05,
    'LINK_SUBSTRATE': 0.05,
}
PRODUCTION_PROBABILITY = 0.95
DISINTEGRATION_PROBABILITY = 0.0005
BONDING_CHAIN_INITIATE_PROBABILITY = 0.1
BONDING_CHAIN_EXTEND_PROBABILITY = 0.6
BONDING_CHAIN_SPLICE_PROBABILITY = 0.9
BOND_DECAY_PROBABILITY = 0.0005
ABSORPTION_PROBABILITY = 0.5
EMISSION_PROBABILITY = 0.5

# Utility functions
def get_neumann_neighborhood(x, y, space_size):
    n = [((x + 1) % space_size, y), ((x - 1) % space_size, y), (x, (y + 1) % space_size), (x, (y - 1) % space_size)]
    return n

def get_random_neumann_neighborhood(x, y, space_size):
    neighborhood = get_neumann_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

def get_moore_neighborhood(x, y, space_size):
    n = [((x - 1) % space_size, (y - 1) % space_size), (x, (y - 1) % space_size), ((x + 1) % space_size, (y - 1) % space_size),
         ((x - 1) % space_size, y), ((x + 1) % space_size, y),
         ((x - 1) % space_size, (y + 1) % space_size), (x, (y + 1) % space_size), ((x + 1) % space_size, (y + 1) % space_size)]
    return n

def get_random_moore_neighborhood(x, y, space_size):
    neighborhood = get_moore_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

def get_random_2_moore_neighborhood(x, y, space_size):
    n0_x, n0_y = get_random_moore_neighborhood(x, y, space_size)
    if x == n0_x:
        n1_x = np.random.choice([(n0_x + 1) % space_size, (n0_x - 1) % space_size])
        n1_y = n0_y
    elif y == n0_y:
        n1_x = n0_y
        n1_y = np.random.choice([(n0_y + 1) % space_size, (n0_y - 1) % space_size])
    else:
        n = [(x, n0_y), (n0_x, y)]
        n1_x, n1_y = n[np.random.randint(len(n))]
    return n0_x, n0_y, n1_x, n1_y

def get_adjacent_moore_neighborhood(x, y, n_x, n_y, space_size):
    if x == n_x:
        n0_x = (n_x - 1) % space_size
        n0_y = n_y
        n1_x = (n_x + 1) % space_size
        n1_y = n_y
    elif y == n_y:
        n0_x = n_x
        n0_y = (n_y - 1) % space_size
        n1_x = n_x
        n1_y = (n_y + 1) % space_size
    else:
        n0_x = x
        n0_y = n_y
        n1_x = n_x
        n1_y = y
    return n0_x, n0_y, n1_x, n1_y

def evaluate_probability(probability):
    return np.random.rand() < probability

def production(particles, x, y, probability):
    p = particles[x, y]
    n0_x, n0_y, n1_x, n1_y = get_random_2_moore_neighborhood(x, y, particles.shape[0])
    n0_p = particles[n0_x, n0_y]
    n1_p = particles[n1_x, n1_y]
    if p['type'] != 'CATALYST' or n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        n0_p['type'] = 'HOLE'
        n1_p['type'] = 'LINK'

def disintegration(particles, x, y, probability):
    p = particles[x, y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        p['disintegrating_flag'] = True
    if not p['disintegrating_flag']:
        return
    emission(particles, x, y, 1.0)
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        bond_decay(particles, x, y, 1.0)
        p['type'] = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating_flag'] = False

def bonding(particles, x, y, chain_initiate_probability, chain_splice_probability, chain_extend_probability, chain_inhibit_bond_flag=True, catalyst_inhibit_bond_flag=True):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] not in ('LINK', 'LINK_SUBSTRATE'):
        return
    if n_p['type'] not in ('LINK', 'LINK_SUBSTRATE'):
        return
    if (n_x, n_y) in p['bonds']:
        return
    if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y, particles.shape[0])
    if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in particles[an1_x, an1_y]['bonds']:
        return
    mn_list = get_moore_neighborhood(x, y, particles.shape[0]) + get_moore_neighborhood(n_x, n_y, particles.shape[0])
    if catalyst_inhibit_bond_flag:
        for mn_x, mn_y in mn_list:
            if particles[mn_x, mn_y]['type'] == 'CATALYST':
                return
    if chain_inhibit_bond_flag:
        for mn_x, mn_y in mn_list:
            if len(particles[mn_x, mn_y]['bonds']) >= 2:
                if (x, y) not in particles[mn_x, mn_y]['bonds'] and (n_x, n_y) not in particles[mn_x, mn_y]['bonds']:
                    return
    if len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
        prob = chain_initiate_probability
    elif len(p['bonds']) == 1 and len(n_p['bonds']) == 1:
        prob = chain_splice_probability
    else:
        prob = chain_extend_probability
    if evaluate_probability(prob):
        p['bonds'].append((n_x, n_y))
        n_p['bonds'].append((x, y))

def bond_decay(particles, x, y, probability):
    p = particles[x, y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        for b in p['bonds']:
            particles[b[0], b[1]]['bonds'].remove((x, y))
        p['bonds'] = []

def absorption(particles, x, y, probability):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        p['type'] = 'LINK_SUBSTRATE'
        n_p['type'] = 'HOLE'

def emission(particles, x, y, probability):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
        return
    if evaluate_probability(probability):
        p['type'] = 'LINK'
        n_p['type'] = 'SUBSTRATE'

# Initialize particles
particles = np.empty((SPACE_SIZE, SPACE_SIZE), dtype=object)
for x in range(SPACE_SIZE):
    for y in range(SPACE_SIZE):
        if evaluate_probability(INITIAL_SUBSTRATE_DENSITY):
            p = {'type': 'SUBSTRATE', 'disintegrating_flag': False, 'bonds': []}
        else:
            p = {'type': 'HOLE', 'disintegrating_flag': False, 'bonds': []}
        particles[x, y] = p

for x, y in INITIAL_CATALYST_POSITIONS:
    particles[x, y]['type'] = 'CATALYST'

def draw_particles():
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x, y]
            color = COLORS[p['type']]
            if p['type'] == 'SUBSTRATE':
                pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
            elif p['type'] == 'CATALYST':
                pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
            elif p['type'] in ('LINK', 'LINK_SUBSTRATE'):
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
                for bond in p['bonds']:
                    bx, by = bond
                    pygame.draw.line(screen, COLORS['LINK'], (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                     (bx * CELL_SIZE + CELL_SIZE // 2, by * CELL_SIZE + CELL_SIZE // 2), 2)
            else:
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def update_particles():
    moved = np.full(particles.shape, False, dtype=bool)
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x, y]
            n_x, n_y = get_random_neumann_neighborhood(x, y, SPACE_SIZE)
            n_p = particles[n_x, n_y]
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])
            if not moved[x, y] and not moved[n_x, n_y] and len(p['bonds']) == 0 and len(n_p['bonds']) == 0 and evaluate_probability(mobility_factor):
                particles[x, y], particles[n_x, n_y] = n_p, p
                moved[x, y] = moved[n_x, n_y] = True

    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            production(particles, x, y, PRODUCTION_PROBABILITY)
            disintegration(particles, x, y, DISINTEGRATION_PROBABILITY)
            bonding(particles, x, y, BONDING_CHAIN_INITIATE_PROBABILITY,
                                     BONDING_CHAIN_SPLICE_PROBABILITY,
                                     BONDING_CHAIN_EXTEND_PROBABILITY)
            bond_decay(particles, x, y, BOND_DECAY_PROBABILITY)
            absorption(particles, x, y, ABSORPTION_PROBABILITY)
            emission(particles, x, y, EMISSION_PROBABILITY)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    update_particles()
    draw_particles()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

```
