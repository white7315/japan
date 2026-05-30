import sys
import json

def calculate_estimation(product_price_jpy, local_shipping_jpy, weight_kg, exchange_rate_krw_100jpy=910.0, usd_to_jpy=155.0):
    """
    일본 구매대행 견적 계산기
    - product_price_jpy: 상품 가격 (엔화)
    - local_shipping_jpy: 일본 내 배송비 (엔화)
    - weight_kg: 예상 무게 (kg)
    - exchange_rate_krw_100jpy: 송금 환율 (100엔당 원화)
    - usd_to_jpy: 과세 판단을 위한 엔-달러 고시환율 (1달러당 엔화)
    """
    # 1. 대행 수수료 책정 (예: 5000엔 미만은 300엔, 이상은 면제)
    proxy_fee = 300 if product_price_jpy < 5000 else 0
    
    # 2. 일본 내 총비용
    japan_total_jpy = product_price_jpy + local_shipping_jpy + proxy_fee
    
    # 3. 한화 환산 (상품가 + 일본배송비 + 수수료)
    exchange_rate_per_jpy = exchange_rate_krw_100jpy / 100.0
    japan_total_krw = round(japan_total_jpy * exchange_rate_per_jpy)
    
    # 4. 국제 배송비 계산 (해운 기준 간이 요율표)
    # 0.5kg 단위 올림
    import math
    billing_weight = math.ceil(weight_kg * 2) / 2
    
    # 기본 0.5kg = 8,500원, 추가 0.5kg당 1,500원 추가
    international_shipping_krw = 8500 + int((billing_weight - 0.5) / 0.5) * 1500 if billing_weight >= 0.5 else 8500
    
    # 5. 관부가세 계산 (면세 한도: 물품 가격이 150 USD 이하)
    # 물품 가격 (JPY) = 상품가 + 일본내 배송비
    items_price_jpy = product_price_jpy + local_shipping_jpy
    items_price_usd = items_price_jpy / usd_to_jpy
    
    tax_duty_krw = 0
    is_taxable = items_price_usd > 150.0
    
    if is_taxable:
        # 일반 의류/잡화 평균 관세 8% 및 부가세 10% 가정
        duty_rate = 0.08
        vat_rate = 0.10
        
        # 과세 가격 = (물품 가격) JPY -> KRW
        customs_value_krw = items_price_jpy * exchange_rate_per_jpy
        
        duty = round(customs_value_krw * duty_rate)
        vat = round((customs_value_krw + duty) * vat_rate)
        tax_duty_krw = duty + vat
    
    # 6. 최종 견적 합계
    total_krw = japan_total_krw + international_shipping_krw + tax_duty_krw
    
    result = {
        "product_price_jpy": product_price_jpy,
        "local_shipping_jpy": local_shipping_jpy,
        "proxy_fee_jpy": proxy_fee,
        "exchange_rate_used": exchange_rate_krw_100jpy,
        "japan_total_jpy": japan_total_jpy,
        "japan_total_krw": japan_total_krw,
        "weight_kg": weight_kg,
        "international_shipping_krw": international_shipping_krw,
        "is_taxable": is_taxable,
        "tax_duty_krw": tax_duty_krw,
        "total_krw": total_krw
    }
    
    return result

if __name__ == "__main__":
    # 테스트 실행
    # 예: 12,000엔 상품, 일본내 배송비 500엔, 무게 1.5kg, 환율 910원
    res = calculate_estimation(12000, 500, 1.5, 910.0)
    print(json.dumps(res, indent=4, ensure_ascii=False))
