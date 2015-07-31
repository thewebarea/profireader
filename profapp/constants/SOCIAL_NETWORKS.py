SOCIAL_NETWORKS = [
    'PROFIREADER',
    'GOOGLE',
    'FACEBOOK',
    'LINKEDIN',
    'TWITTER',
    'MICROSOFT',
    'YAHOO',
]

SOC_NET_FIELDS = [
    'ID',
    'EMAIL',
    'FIRST_NAME',
    'LAST_NAME',
    'NAME',
    'GENDER',
    'LINK',
    'PHONE',
]

SOC_NET_NONE = dict((soc_net,
                     dict((field, None)
                          for field in SOC_NET_FIELDS))
                    for soc_net in SOCIAL_NETWORKS)

DB_FIELDS = dict((soc_net,
                dict((field, (soc_net+'_'+field).lower())
                     for field in SOC_NET_FIELDS))
                for soc_net in SOCIAL_NETWORKS)
