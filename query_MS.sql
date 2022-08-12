Select
    b.ID_BET "BetId",

    Max(Cast(cli.REGISTRATION_DATETIME as Datetime2(0))) "RegDate",

    Max(b.ID_ORDER)                                    "OrderId",
    Max(d.BARCODE)                                     "BARCODE",
    Max(Cast(d.CORE_CREATE_DATETIME  as Datetime2(0))) "CreateDate",
    Max(cli.CLIENT_NUMBER)                             "ClientNumber",

    Cast(Max(b.BET_SUM) - Max(b.WIN_SUM) as Money) "Profit",
    Cast(Max(b.BET_SUM) as Money)                  "Turnover"

from Core.dbo.DIC_BET b
left join Core.dbo.FCT_ORDER o on o.ID_ORDER = b.ID_ORDER
left join Core.dbo.DIC_DOCUMENT d on d.ID_DOCUMENT = o.ID_DOCUMENT
left join Core.dbo.DIC_CLIENT_ACCOUNT c on c.ID_CLIENT_ACCOUNT = d.ID_CLIENT_ACCOUNT
left join Core.dbo.DIC_CLIENT cli on cli.ID_CLIENT = c.ID_CLIENT

where b.CORE_CREATE_DATETIME between '<period1>' and '<period2>'
and cli.Client_Number in (<client_number>)
and cli.IS_NOT_VALID = 0
    
Group By b.ID_BET