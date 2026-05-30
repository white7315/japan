import sqlite3
import os

# 데이터베이스 경로 설정
DB_PATH = r"E:\japan-proxy-shopping\proxy_shopping.db"

def calculate_estimated_krw(price_jpy, exchange_rate=9.1, shipping_krw=8500):
    # 5000엔 이상 수수료 면제, 미만 300엔
    proxy_fee = 0 if price_jpy >= 5000 else 300
    japan_total_krw = (price_jpy + proxy_fee) * exchange_rate
    # 관세 계산 (150달러 초과 시 대략 23,000엔 이상일 때 관세가 붙는다고 가정)
    tax_duty_krw = 0
    if price_jpy > 23000:
        # 약 18% 관부가세 적용 가정
        tax_duty_krw = round(price_jpy * exchange_rate * 0.18)
    
    total_krw = round(japan_total_krw) + shipping_krw + tax_duty_krw
    return total_krw

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sourced_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_url TEXT UNIQUE,
        original_title TEXT,
        translated_title TEXT,
        price_jpy INTEGER,
        estimated_krw INTEGER,
        original_description TEXT,
        translated_description TEXT,
        status TEXT DEFAULT 'Sourced',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    return conn

def insert_sample_data(conn):
    cursor = conn.cursor()
    
    # 10개의 인기 피규어 및 주변 도구 소싱 데이터
    samples = [
        {
            "url": "https://jp.mercari.com/item/m112233445",
            "orig_title": "【未開封・美品】ブルーアーカイブ 砂狼シロコ ねんどろいど",
            "trans_title": "[미개봉/미품] 블루 아카이브 스나오오카미 시로코 넨도로이드",
            "price": 6800,
            "orig_desc": "ブルーアーカイブ 砂狼シロコのねんどろいどです。購入後、暗所にて保管しておりました。箱にも目立つ傷はありません。即購入大歓迎です。",
            "trans_desc": "블루 아카이브 스나오오카미 시로코 넨도로이드입니다. 구매 후 암소에서 보관해 왔습니다. 박스에도 눈에 띄는 큰 상처는 없습니다. 즉시 구매 환영합니다."
        },
        {
            "url": "https://jp.mercari.com/item/m998877665",
            "orig_title": "フィギュアケース J-STAGE LED照明・背面ミラー付き",
            "trans_title": "[중고 미품] 피규어 케이스 J-STAGE (LED 조명 및 뒷면 거울 모델)",
            "price": 11500,
            "orig_desc": "アクリルケース J-STAGEのLED・背面ミラーモデルです。半年ほどフィギュアを飾るのに使用。目立つ傷やアクリルの割れはありません。LED点灯確認済み。電源コード付属。",
            "trans_desc": "아크릴 케이스 J-STAGE LED 및 뒷면 거울 모델입니다. 반년 정도 피규어를 전시하는 데 사용했습니다. 눈에 띄는 흠집이나 아크릴 깨짐은 없습니다. LED 정상 작동 확인됨. 전원 코드 포함."
        },
        {
            "url": "https://jp.mercari.com/item/m554433221",
            "orig_title": "【パーツ欠品なし・美品】ねんどろいど アロナ ブルーアーカイブ",
            "trans_title": "[개봉품/부품완비] 블루 아카이브 아로나 넨도로이드",
            "price": 5400,
            "orig_desc": "ブルーアーカイブ アロナのねんどろいどです。パーツ欠品なし。一度組み立ててガラスケース内に飾っていました。日焼けやベタつきはなく綺麗な状態です。",
            "trans_desc": "블루 아카이브 아로나 넨도로이드입니다. 부품 결품 없음. 한 번 조립하여 유리 케이스 내부에 진열해 두었습니다. 빛바램이나 끈적임 없이 깨끗한 상태입니다."
        },
        {
            "url": "https://jp.mercari.com/item/m111111111",
            "orig_title": "【未開封・美品】ねんどろいど 美甘ネル ブルーアーカイブ",
            "trans_title": "[미개봉/미품] 블루 아카이브 미카모 네루 넨도로이드",
            "price": 6200,
            "orig_desc": "ブルーアーカイブ 美甘ネルのねんどろいどです。未開封品。国内正規品。購入後プチプチに包んで暗所保管していました。",
            "trans_desc": "블루 아카이브 미카모 네루 넨도로이드입니다. 미개봉품. 국내 정품. 구매 후 에어캡에 포장하여 어두운 곳에 보관했습니다."
        },
        {
            "url": "https://jp.mercari.com/item/m222222222",
            "orig_title": "【未開封】聖園ミカ ねんどろいど グッスマ特典付き",
            "trans_title": "[미개봉/특전포함] 블루 아카이브 미소노 미카 넨도로이드",
            "price": 7200,
            "orig_desc": "ねんどろいど ブルーアーカイブ 聖園ミカ。グッドスマイルカンパニー公式ショップ特典(背景シート)付き、新品未開封です。",
            "trans_desc": "블루 아카이브 미소노 미카 넨도로이드. 굿스마 공식숍 특전(배경 시트)이 포함되어 있으며, 새 상품 미개봉 상태입니다."
        },
        {
            "url": "https://jp.mercari.com/item/m333333333",
            "orig_title": "METAL BUILD フリーダムガンダム CONCEPT 2",
            "trans_title": "[중고 최고급] 메탈빌드 프리덤 건담 CONCEPT 2 (관절 우수)",
            "price": 28000,
            "orig_desc": "【中古美品】メタルビルド フリーダムガンダム CONCEPT 2. 開封品ですが欠品なし、関節の緩みもありません。コレクション整理のため出品します。",
            "trans_desc": "[중고 미품] 메탈 빌드 프리덤 건담 CONCEPT 2. 개봉 품이나 빠진 부품 없으며 관절 헐거움 없습니다. 장식 정리를 위해 출품합니다. (관세 포함 계산)"
        },
        {
            "url": "https://jp.mercari.com/item/m444444444",
            "orig_title": "【未開封】一番くじ ワンピース A賞 ルフィ フィギュア",
            "trans_title": "[미개봉 신품] 제일복권 원피스 A상 루피 피규어",
            "price": 4500,
            "orig_desc": "一番くじ ワンピース A賞 モンキー・D・ルフィ フィギュアです。新品未開封品になります。店頭受け取り後すぐに保管しました。",
            "trans_desc": "제일복권 원피스 A상 몽키 D 루피 피규어입니다. 새 상품 미개봉품입니다. 매장에서 수령 후 즉시 어두운 곳에 보관했습니다."
        },
        {
            "url": "https://jp.mercari.com/item/m555555555",
            "orig_title": "ミュージアムジェル 100g フィギュア 転倒防止",
            "trans_title": "[미술관용] 피규어 전도 방지 뮤지엄 겔 100g (지진 대비용)",
            "price": 2100,
            "orig_desc": "【新品】フィギュア・コレクションケース用転倒防止ミュージアムジェル 100g。透明で目立ちません。地震対策に必須です。",
            "trans_desc": "[새상품] 피규어 및 컬렉션 케이스용 전도 방지 뮤지엄 겔 100g. 투명하여 티가 나지 않습니다. 지진 대책 및 진열장 낙하 방지에 필수입니다."
        },
        {
            "url": "https://jp.mercari.com/item/m666666666",
            "orig_title": "タミヤ クラフトツール 静電気防止 モデルクリーニングブラシ",
            "trans_title": "[먼지 제거] 타미야 크래프트 툴 정전기 방지 브러시 (새제품)",
            "price": 1800,
            "orig_desc": "【新品】タミヤ モデルクリーニングブラシ 静電気防止タイプ。フィギュアやプラモデルのホコリ取りに最適です。",
            "trans_desc": "[새상품] 타미야 모델 클리닝 브러시 정전기 방지 타입. 피규어 및 프라모델의 미세 먼지 제거에 가장 적합한 고성능 브러시입니다."
        },
        {
            "url": "https://jp.mercari.com/item/m777777777",
            "orig_title": "【未開封・美品】ねんどろいど 早瀬ユウカ ブルーアーカイブ",
            "trans_title": "[미개봉/미품] 블루 아카이브 하야세 유우카 넨도로이드",
            "price": 6500,
            "orig_desc": "ブルーアーカイブ 早瀬ユウカ のねんどろいど。あみあみで購入後、未開封のまま段ボール内で保管しておりました。極めて美品です。",
            "trans_desc": "블루 아카이브 하야세 유우카 넨도로이드. 아미아미에서 구매한 후, 미개봉 상태로 종이박스에 넣어 보관했습니다. 매우 좋은 상태입니다."
        }
    ]
    
    inserted_count = 0
    for s in samples:
        estimated_krw = calculate_estimated_krw(s["price"])
        try:
            cursor.execute("""
            INSERT OR REPLACE INTO sourced_items (
                source_url, original_title, translated_title, 
                price_jpy, estimated_krw, original_description, translated_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (s["url"], s["orig_title"], s["trans_title"], s["price"], estimated_krw, s["orig_desc"], s["trans_desc"]))
            inserted_count += 1
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    print(f"새로운/업데이트된 상품 {inserted_count}개가 소싱 DB에 등록되었습니다.")

def print_sourced_items(conn, limit=10):
    cursor = conn.cursor()
    cursor.execute("SELECT id, translated_title, price_jpy, estimated_krw, status FROM sourced_items LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    print(f"\n================== 현재 소싱된 상품 목록 (SQLite DB - 최대 {limit}개) ==================")
    print(f"{'ID':<4} | {'상품명':<40} | {'현지가 (엔화)':<10} | {'원화 견적':<10} | {'상태':<10}")
    print("-" * 90)
    for row in rows:
        print(f"{row[0]:<4} | {row[1][:38]:<40} | {row[2]:<10,} | {row[3]:<10,} | {row[4]:<10}")
    print("========================================================================\n")

if __name__ == "__main__":
    conn = init_db()
    insert_sample_data(conn)
    print_sourced_items(conn, 10)
    conn.close()
