import requests
import json
import time
import logging
from threading import Thread
from Queue import Queue
from datetime import datetime, date, timedelta

class Stock(object):
    default_log_path = '/tmp/stock.log'
    index_list = {'taiex': 'tse_t00.tw', 'tpex': 'otc_o00.tw', 'frmsa': 'tse_FRMSA.tw'}
    tse_list = ['0050', '0051', '0052', '0053', '0054', '0055', '0056', '0057', '0058', '0059', '0061', '006203', '006204', '006205', '006206', '006207', '006208', '00631L', '00632R', '00633L', '00634R', '00635U', '00636', '00637L', '00638R', '00639', '00640L', '00641R', '00642U', '00643', '00645', '00646', '00647L', '00648R', '00649', '00650L', '00651R', '00652', '00653L', '00654R', '00655L', '00656R', '008201', '1101', '1102', '1103', '1104', '1108', '1109', '1110', '1201', '1203', '1210', '1213', '1215', '1216', '1217', '1218', '1219', '1220', '1225', '1227', '1229', '1231', '1232', '1233', '1234', '1235', '1236', '1262', '1301', '1303', '1304', '1305', '1307', '1308', '1309', '1310', '1312', '1313', '1314', '1315', '1319', '1321', '1323', '1324', '1325', '1326', '1337', '1338', '1339', '1340', '1402', '1409', '1410', '1414', '1416', '1417', '1419', '1423', '1432', '1434', '1436', '1437', '1439', '1440', '1442', '1444', '1445', '1446', '1447', '1451', '1452', '1453', '1454', '1455', '1457', '1459', '1460', '1463', '1464', '1465', '1466', '1467', '1470', '1471', '1473', '1474', '1476', '1477', '1503', '1504', '1506', '1507', '1513', '1514', '1515', '1516', '1517', '1519', '1521', '1522', '1524', '1525', '1526', '1527', '1528', '1530', '1531', '1532', '1533', '1535', '1536', '1537', '1539', '1540', '1541', '1558', '1560', '1568', '1582', '1583', '1589', '1590', '1592', '1603', '1604', '1605', '1608', '1609', '1611', '1612', '1614', '1615', '1617', '1618', '1626', '1701', '1702', '1704', '1707', '1708', '1709', '1710', '1711', '1712', '1713', '1714', '1715', '1717', '1718', '1720', '1722', '1723', '1724', '1725', '1726', '1727', '1729', '1730', '1731', '1732', '1733', '1734', '1735', '1736', '1737', '1762', '1773', '1783', '1786', '1789', '1802', '1806', '1808', '1809', '1810', '1817', '1902', '1903', '1904', '1905', '1906', '1907', '1909', '2002', '2006', '2008', '2010', '2012', '2013', '2015', '2020', '2023', '2024', '2027', '2029', '2030', '2031', '2032', '2033', '2034', '2038', '2049', '2059', '2062', '2101', '2102', '2103', '2104', '2105', '2106', '2107', '2108', '2109', '2114', '2115', '2201', '2204', '2206', '2207', '2208', '2227', '2228', '2231', '2301', '2302', '2303', '2308', '2311', '2312', '2313', '2316', '2317', '2323', '2324', '2325', '2327', '2328', '2329', '2330', '2331', '2332', '2338', '2340', '2344', '2345', '2347', '2351', '2352', '2353', '2354', '2355', '2356', '2357', '2359', '2360', '2362', '2363', '2365', '2367', '2368', '2369', '2371', '2373', '2374', '2375', '2376', '2377', '2379', '2380', '2382', '2383', '2385', '2387', '2390', '2392', '2393', '2395', '2397', '2399', '2401', '2402', '2404', '2405', '2406', '2408', '2409', '2412', '2413', '2414', '2415', '2417', '2419', '2420', '2421', '2423', '2424', '2425', '2426', '2427', '2428', '2430', '2431', '2433', '2436', '2437', '2439', '2441', '2442', '2443', '2448', '2449', '2450', '2451', '2453', '2454', '2455', '2456', '2457', '2458', '2459', '2460', '2461', '2462', '2464', '2466', '2467', '2468', '2471', '2472', '2474', '2476', '2477', '2478', '2480', '2481', '2482', '2483', '2484', '2485', '2486', '2488', '2489', '2492', '2493', '2495', '2497', '2498', '2499', '2501', '2504', '2505', '2506', '2509', '2511', '2514', '2515', '2516', '2520', '2524', '2527', '2528', '2530', '2534', '2535', '2536', '2537', '2538', '2539', '2540', '2542', '2543', '2545', '2546', '2547', '2548', '2597', '2601', '2603', '2605', '2606', '2607', '2608', '2609', '2610', '2611', '2612', '2613', '2615', '2616', '2617', '2618', '2634', '2637', '2642', '2701', '2702', '2704', '2705', '2706', '2707', '2712', '2722', '2723', '2727', '2731', '2801', '2809', '2812', '2816', '2820', '2823', '2832', '2834', '2836', '2838', '2841', '2845', '2849', '2850', '2851', '2852', '2855', '2856', '2867', '2880', '2881', '2882', '2883', '2884', '2885', '2886', '2887', '2888', '2889', '2890', '2891', '2892', '2901', '2903', '2904', '2905', '2906', '2908', '2910', '2911', '2912', '2913', '2915', '2929', '3002', '3003', '3004', '3005', '3006', '3008', '3010', '3011', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3021', '3022', '3023', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3035', '3036', '3037', '3038', '3040', '3041', '3042', '3044', '3045', '3047', '3048', '3049', '3050', '3052', '3054', '3055', '3056', '3057', '3058', '3059', '3060', '3062', '3090', '3094', '3130', '3149', '3164', '3167', '3189', '3209', '3229', '3231', '3257', '3266', '3296', '3305', '3308', '3311', '3312', '3315', '3338', '3356', '3376', '3380', '3383', '3406', '3413', '3416', '3419', '3432', '3437', '3443', '3450', '3454', '3474', '3481', '3494', '3501', '3504', '3514', '3515', '3518', '3519', '3533', '3545', '3550', '3559', '3561', '3573', '3576', '3579', '3583', '3588', '3591', '3596', '3598', '3605', '3607', '3617', '3622', '3645', '3653', '3661', '3665', '3669', '3673', '3679', '3682', '3686', '3694', '3698', '3702', '3703', '3704', '3705', '3706', '4104', '4106', '4108', '4119', '4133', '4137', '4141', '4142', '4144', '4164', '4306', '4414', '4426', '4526', '4532', '4536', '4551', '4720', '4722', '4725', '4733', '4737', '4746', '4755', '4904', '4906', '4912', '4915', '4916', '4919', '4927', '4930', '4934', '4935', '4938', '4942', '4952', '4956', '4958', '4960', '4976', '4977', '4984', '4994', '4999', '5007', '5203', '5215', '5225', '5234', '5243', '5264', '5269', '5285', '5288', '5305', '5388', '5434', '5469', '5471', '5515', '5519', '5521', '5522', '5525', '5531', '5533', '5534', '5538', '5607', '5608', '5706', '5871', '5880', '5907', '6005', '6108', '6112', '6115', '6116', '6117', '6120', '6128', '6131', '6133', '6136', '6141', '6142', '6145', '6152', '6153', '6155', '6164', '6166', '6168', '6176', '6177', '6183', '6184', '6189', '6191', '6192', '6196', '6197', '6201', '6202', '6205', '6206', '6209', '6213', '6214', '6215', '6216', '6224', '6226', '6230', '6239', '6243', '6251', '6257', '6269', '6271', '6277', '6278', '6281', '6282', '6285', '6286', '6405', '6409', '6412', '6414', '6415', '6422', '6431', '6442', '6449', '6451', '6452', '6456', '6504', '6505', '6605', '6702', '8011', '8016', '8021', '8039', '8046', '8070', '8072', '8081', '8101', '8103', '8105', '8110', '8112', '8114', '8131', '8150', '8163', '8201', '8210', '8213', '8215', '8222', '8249', '8261', '8271', '8341', '8374', '8404', '8411', '8422', '8427', '8429', '8443', '8454', '8463', '8464', '8926', '8940', '8996', '9103', '910482', '9105', '910801', '911616', '9136', '9188', '9802', '9902', '9904', '9905', '9906', '9907', '9908', '9910', '9911', '9912', '9914', '9917', '9918', '9919', '9921', '9924', '9925', '9926', '9927', '9930', '9931', '9933', '9934', '9937', '9938', '9939', '9940', '9941', '9942', '9943', '9944', '9945', '9946', '9955', '9958']
    otc_list = ['1258', '1259', '1264', '1333', '1336', '1565', '1566', '1569', '1570', '1580', '1584', '1586', '1591', '1593', '1595', '1597', '1599', '1742', '1752', '1777', '1781', '1784', '1787', '1788', '1795', '1799', '1813', '1815', '2035', '2061', '2063', '2064', '2066', '2067', '2221', '2230', '2233', '2235', '2596', '2636', '2640', '2641', '2643', '2718', '2719', '2724', '2726', '2729', '2732', '2734', '2736', '2740', '2916', '2924', '2926', '2928', '3064', '3066', '3067', '3068', '3071', '3073', '3078', '3081', '3083', '3085', '3086', '3088', '3089', '3092', '3093', '3095', '3105', '3114', '3115', '3118', '3122', '3128', '3131', '3141', '3144', '3152', '3162', '3163', '3169', '3171', '3176', '3188', '3191', '3202', '3205', '3206', '3207', '3211', '3213', '3217', '3218', '3219', '3221', '3224', '3226', '3227', '3228', '3230', '3232', '3234', '3236', '3252', '3259', '3260', '3264', '3265', '3268', '3272', '3276', '3284', '3285', '3287', '3288', '3289', '3290', '3291', '3293', '3294', '3297', '3299', '3303', '3306', '3310', '3313', '3317', '3322', '3323', '3324', '3325', '3332', '3339', '3354', '3360', '3362', '3363', '3372', '3373', '3374', '3379', '3388', '3390', '3402', '3428', '3431', '3434', '3438', '3441', '3444', '3452', '3455', '3465', '3466', '3479', '3483', '3484', '3489', '3490', '3491', '3492', '3498', '3499', '3508', '3511', '3512', '3516', '3520', '3521', '3522', '3523', '3526', '3527', '3529', '3531', '3537', '3540', '3541', '3546', '3548', '3551', '3552', '3553', '3555', '3556', '3558', '3562', '3563', '3564', '3567', '3570', '3577', '3580', '3581', '3587', '3594', '3609', '3611', '3615', '3623', '3624', '3625', '3628', '3629', '3630', '3631', '3632', '3642', '3646', '3652', '3658', '3662', '3663', '3664', '3666', '3672', '3675', '3680', '3684', '3685', '3687', '3689', '3691', '3693', '3707', '4102', '4103', '4105', '4107', '4109', '4111', '4113', '4114', '4116', '4120', '4121', '4123', '4126', '4127', '4128', '4129', '4130', '4131', '4138', '4139', '4147', '4152', '4153', '4154', '4157', '4160', '4161', '4162', '4163', '4167', '4168', '4171', '4173', '4174', '4175', '4180', '4188', '4192', '4198', '4205', '4207', '4303', '4304', '4305', '4401', '4402', '4406', '4413', '4415', '4416', '4417', '4419', '4420', '4429', '4430', '4432', '4433', '4502', '4503', '4506', '4510', '4513', '4523', '4527', '4528', '4529', '4530', '4533', '4534', '4535', '4541', '4542', '4543', '4549', '4550', '4556', '4609', '4702', '4706', '4707', '4711', '4712', '4714', '4716', '4721', '4726', '4728', '4729', '4735', '4736', '4739', '4743', '4745', '4747', '4762', '4803', '4804', '4806', '4903', '4905', '4907', '4908', '4909', '4911', '4924', '4933', '4939', '4944', '4946', '4947', '4950', '4953', '4965', '4966', '4971', '4972', '4973', '4974', '4979', '4987', '4991', '4995', '5009', '5011', '5013', '5014', '5015', '5016', '5102', '5201', '5202', '5205', '5206', '5209', '5210', '5211', '5212', '5213', '5227', '5230', '5245', '5251', '5255', '5263', '5272', '5274', '5276', '5278', '5281', '5284', '5287', '5289', '5291', '5301', '5302', '5304', '5306', '5309', '5310', '5312', '5314', '5315', '5317', '5321', '5324', '5328', '5340', '5344', '5345', '5347', '5348', '5349', '5351', '5353', '5355', '5356', '5364', '5371', '5381', '5383', '5384', '5386', '5392', '5398', '5403', '5410', '5425', '5426', '5432', '5438', '5439', '5443', '5450', '5452', '5455', '5457', '5460', '5464', '5465', '5468', '5474', '5475', '5478', '5480', '5481', '5483', '5487', '5488', '5489', '5490', '5491', '5493', '5498', '5508', '5511', '5512', '5514', '5516', '5520', '5523', '5529', '5530', '5536', '5543', '5601', '5603', '5604', '5609', '5701', '5703', '5704', '5820', '5878', '5902', '5903', '5904', '5905', '6015', '6016', '6020', '6021', '6022', '6023', '6024', '6026', '6101', '6103', '6104', '6105', '6107', '6109', '6111', '6113', '6114', '6118', '6121', '6122', '6123', '6124', '6125', '6126', '6127', '6129', '6130', '6134', '6138', '6140', '6143', '6144', '6146', '6147', '6148', '6150', '6151', '6154', '6156', '6158', '6160', '6161', '6163', '6167', '6169', '6170', '6171', '6173', '6174', '6175', '6179', '6180', '6182', '6185', '6186', '6187', '6188', '6190', '6194', '6195', '6198', '6199', '6203', '6204', '6207', '6208', '6210', '6212', '6217', '6218', '6219', '6220', '6221', '6223', '6227', '6228', '6229', '6231', '6233', '6234', '6236', '6237', '6238', '6241', '6242', '6244', '6245', '6246', '6247', '6248', '6259', '6261', '6263', '6264', '6265', '6266', '6270', '6274', '6275', '6276', '6279', '6284', '6287', '6290', '6291', '6292', '6294', '6298', '6404', '6411', '6417', '6419', '6426', '6432', '6435', '6457', '6462', '6465', '6469', '6470', '6482', '6485', '6488', '6494', '6496', '6506', '6508', '6509', '6510', '6512', '6514', '6523', '6603', '6609', '6803', '7402', '8024', '8027', '8032', '8034', '8038', '8040', '8042', '8043', '8044', '8047', '8048', '8049', '8050', '8054', '8059', '8064', '8066', '8067', '8068', '8069', '8071', '8074', '8076', '8077', '8079', '8080', '8082', '8083', '8084', '8085', '8086', '8087', '8088', '8091', '8092', '8093', '8096', '8097', '8099', '8107', '8109', '8111', '8121', '8147', '8155', '8171', '8176', '8182', '8183', '8234', '8240', '8255', '8266', '8277', '8287', '8289', '8291', '8299', '8349', '8354', '8358', '8383', '8390', '8401', '8403', '8406', '8409', '8410', '8416', '8418', '8420', '8421', '8423', '8424', '8426', '8431', '8432', '8433', '8435', '8436', '8437', '8444', '8446', '8450', '8455', '8462', '8472', '8905', '8906', '8908', '8913', '8916', '8917', '8921', '8923', '8924', '8927', '8928', '8929', '8930', '8931', '8932', '8933', '8934', '8935', '8936', '8937', '8938', '8941', '8942', '9949', '9950', '9951', '9960', '9962']
    api_entry = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp'
    query_count = 100
    timeout = 10

    def __init__(self, numbers=None, **kwargs):
        ''' supported argument:
            from_data, log, log.
        '''
        self.queue = Queue()
        self.numbers = numbers
        self.from_date = kwargs.get('from_date')
        self.db = kwargs.get('db')
        self.log = kwargs.get('log') if kwargs.get('log') is not None else self._get_default_logging()
        self.query_params = self._to_query_params(numbers)

        if self.from_date is None:
            self.raw = self._get_latest()
        else:
            self.raw = self._get_from_date()

        self.data = self._raw2data(self.raw)
     
    def _get_default_logging(self):
        logging.basicConfig(filename=self.default_log_path, level=logging.DEBUG)
        return logging

    def _to_query_params(self, numbers):
        idx = 0    
        query_params = []
        query_strings = []

        if numbers is None:
            query_strings.extend([value for key, value in self.index_list.items()])
            query_strings.extend(['tse_{}.tw'.format(number) for number in self.tse_list]) 
            query_strings.extend(['otc_{}.tw'.format(number) for number in self.otc_list])  
        else:
            for number in numbers:
                if self.index_list.get(number) is not None:
                    number = self.index_list.get(number)
                elif number in self.tse_list:
                    number = 'tse_{}.tw'.format(number)
                elif number in self.otc_list:
                    number = 'otc_{}.tw'.format(number)
                else:
                    self.error = 'Invalid stock number ' + number
                    continue

                query_strings.append(number)

        length = len(query_strings)

        while idx < length:
            ex_ch = '|'.join(query_strings[idx:idx + self.query_count])
            query_params.append(ex_ch)
            idx += self.query_count

        return query_params

    def _get_latest(self):
        self.log.info("start to fetch latest data at %s", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        raw = []
        threads = []

        for ex_ch in self.query_params:
            thread = Thread(target=self._get, args=({'ex_ch': ex_ch},))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        while not self.queue.empty():
            raw.extend(self.queue.get())

        self.log.info('Totally retrieve %s stock information', len(raw))
        return raw

    def _get_from_date(self):
        raws = []
        from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
        dd = date.today() - from_date

        for i in range(dd.days + 1):
            day = from_date + timedelta(days=i)
                
            if day.isoweekday() == 6 or day.isoweekday() == 7:
                continue

            self.log.info("start to fetch %s history data at %s", day.strftime('%Y-%m-%d'), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            threads = []
            raw = []
            d = day.strftime('%Y%m%d')

            for ex_ch in self.query_params:
                thread = Thread(target=self._get, args=({'ex_ch': ex_ch, 'd': d},))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            while not self.queue.empty():
                raw.extend(self.queue.get())

            try:
                if not self.db:
                    raws.extend(raw)
                else:
                    self.db.commit_history(self._raw2data(raw))
            except Exception as e:
                self.log.warning("%s", e)
                continue

        return raws

    def _get(self, params):
        client = requests.session()

        try:
            client.get(self.api_entry, timeout=self.timeout)
            r = client.get(self.api_entry, params=params, timeout=self.timeout)
            self.log.debug('fetch data from %s', r.url)
        except Exception as e:
            self.log.warning('(X) Timeout %s', params)
            raise e

        try:
            raw = json.loads(r.content).get('msgArray')
        except Exception as e:
            self.log.warning('(X) Retrun Data is not JSON', params)
            raise e 

        self.log.info('Retrieve %s stock information', len(raw))
        self.queue.put(raw)

    def _raw2data(self, raw):
        data = []
        updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        for row in raw:
            number = row.get('c')

            if not number:
                continue

            data.append({
                'number': number,
                'type': row.get('ex'),
                'name': row.get('n'),
                'latest_price': row.get('z', -1),
                'highest_price': row.get('h', -1),
                'lowest_price': row.get('l', -1),
                'opening_price': row.get('o', -1),
                'limit_up': row.get('u', -1),
                'limit_down': row.get('w', -1),
                'yesterday_price': row.get('y', -1),
                'temporal_volume': self._to_number(row.get('tv', -1)),
                'volume': row.get('v', -1),
                'top5_sold_prices': self._to_json(row.get('a', '')),
                'top5_sold_count': self._to_json(row.get('f', '')),
                'top5_buy_prices': self._to_json(row.get('b', '')),
                'top5_buy_count': self._to_json(row.get('g', '')),
                'record_time': self._to_datetime(row.get('tlong'), row.get('d'), row.get('t')),
                'updated_at': updated_at,
            })

        return data

    def _to_number(self, number):
        return -1 if number == '-' else number

    def _to_json(self, string):
        return json.dumps(string.split('_')[:-1])

    def _to_datetime(self, tlong, d, t):
        datetime = None

        if tlong is not None:
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(tlong) / 1000))
        else:
            datetime = '{0}-{1}-{2} {3}'.format(d[0:4], d[4:6], d[6:], t)

        return datetime