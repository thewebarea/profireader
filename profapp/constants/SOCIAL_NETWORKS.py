SOCIAL_NETWORKS = [
    'profireader',
    'google',
    'facebook',
    'linkedin',
    'twitter',
    'microsoft',
    'yahoo',
]

SOC_NET_FIELDS = [
    'id',
    'email',
    'first_name',
    'last_name',
    'name',
    'gender',
    'link',
    'phone',
]

INFO_ITEMS_NONE = dict((field, '') for field in SOC_NET_FIELDS)

SOC_NET_NONE = dict((soc_net, INFO_ITEMS_NONE)
                    for soc_net in SOCIAL_NETWORKS)

# for soc_net in SOCIAL_NETWORKS:
#     SOC_NET_NONE[soc_net].update(dict([('phone', '')]))

DB_FIELDS = dict((soc_net,
                 dict((field, (soc_net+'_'+field))
                      for field in SOC_NET_FIELDS))
                 for soc_net in SOCIAL_NETWORKS)
