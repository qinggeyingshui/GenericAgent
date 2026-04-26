"""自媒体变现策略工具 - 支持广告收益计算/品牌报价/会员定价"""

def calc_ad_revenue(views: int, cpm: float = 5.0, ctr: float = 0.02, cpc: float = 0.5) -> dict:
    """广告收益计算
    Args:
        views: 播放/阅读量
        cpm: 千次展示收益(元), 默认5元
        ctr: 点击率, 默认2%
        cpc: 单次点击收益(元), 默认0.5元
    Returns: 展示收益、点击收益、总收益
    """
    impression_rev = views * cpm / 1000
    click_rev = views * ctr * cpc
    return {"展示收益": round(impression_rev, 2), "点击收益": round(click_rev, 2), 
            "总收益": round(impression_rev + click_rev, 2), "预估CPM": cpm}

def calc_brand_quote(followers: int, engagement_rate: float = 0.03, category: str = "通用") -> dict:
    """品牌合作报价计算
    Args:
        followers: 粉丝数
        engagement_rate: 互动率(点赞+评论+转发/粉丝数), 默认3%
        category: 领域(科技/美妆/生活/通用), 影响溢价系数
    Returns: 基础报价、推荐报价区间
    """
    # 领域溢价系数
    multipliers = {"科技": 1.2, "美妆": 1.5, "生活": 1.0, "财经": 1.3, "通用": 1.0}
    m = multipliers.get(category, 1.0)
    # 基础公式: 粉丝数 * 0.03-0.1元 * 互动率加成 * 领域系数
    base = followers * 0.05 * (1 + engagement_rate * 10) * m
    return {"基础报价": round(base, 0), "报价区间": [round(base * 0.7, 0), round(base * 1.3, 0)],
            "互动率加成": f"{engagement_rate*100:.1f}%", "领域系数": m}

def calc_membership_price(content_freq: int, exclusive_ratio: float = 0.3, market_avg: float = 30) -> dict:
    """会员定价策略
    Args:
        content_freq: 月更新频次
        exclusive_ratio: 会员专属内容占比, 默认30%
        market_avg: 同类市场均价(元/月), 默认30元
    Returns: 建议月费、年费、定价依据
    """
    # 内容频次加成 + 专属比例加成
    price = market_avg * (1 + content_freq / 30) * (1 + exclusive_ratio)
    annual = price * 10  # 年费8.3折
    return {"建议月费": round(price, 0), "建议年费": round(annual, 0),
            "折扣力度": "年费约8.3折", "定价依据": f"基于{content_freq}次/月更新+{exclusive_ratio*100:.0f}%专属内容"}

if __name__ == "__main__":
    # 测试
    print("=== 广告收益测试 ===")
    print(calc_ad_revenue(100000))
    print("\n=== 品牌报价测试 ===")
    print(calc_brand_quote(50000, 0.05, "科技"))
    print("\n=== 会员定价测试 ===")
    print(calc_membership_price(8, 0.4))
