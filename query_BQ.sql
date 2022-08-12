SELECT
    o.id,
    o.userid,
    o.date OrderDate,

    h.date HitDate,
    h.context.campaign.medium,
    h.context.campaign.source,
    h.context.campaign.name,
    h.context.campaign.content,
    h.context.campaign.term,

    DATE_DIFF(o.date, h.date, day) DatesDiff

FROM warm-actor-290215.segmentstream_202203.orders o
LEFT JOIN warm-actor-290215.segmentstream_202203.hitsSet h ON h.anonymousId = o.attributedAnonymousId

WHERE o.date BETWEEN "<period_order1>" AND "<period_order2>"
AND h.date BETWEEN "<period_hit1>" AND "<period_hit2>"
AND DATE_DIFF(o.date, h.date, day) <= 15
AND DATE_DIFF(o.date, h.date, day) >= 0
AND h.context.campaign.medium IN ('cpm', 'cpc', 'referral')
AND h.context.campaign.source IN (<source>)
