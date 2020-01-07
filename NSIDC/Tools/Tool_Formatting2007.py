import numpy as np


def looop():
	year = 2007
	month = 2
	day = 28
	
	
	for count in range (0,2,1): #366
		filename = str(year)+'/NSIDC_'+str(year)+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename2 = 'NSIDC_'+str(year)+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		try:
			with open(filename, 'rb') as fr:
				#hdr = fr.read(300)
				ice = np.fromfile(fr, dtype=np.uint8)
		except:
			print('cant read')
			
		icepoleedge = [67639,67335,67942,67941,67640,67336,67641,67337,67642,67338,67643,67339,67644,67340,67645,67341,67646,67342,67951,67952,67941,67637,68244,68243,67942,67638,67951,67647,67952,67648,68257,68258,68243,67939,68546,68545,68244,67940,68257,67953,68258,67954,68563,68564,68546,68242,68849,68848,68563,68259,68868,68869,68849,68545,69152,69151,68868,68564,69173,69174,69456,69455,69477,69478,69456,69152,69759,69758,69477,69173,69782,69783,70063,70062,70086,70087,70063,69759,70366,70365,70086,69782,70391,70392,70670,70669,70695,70696,70974,70973,70999,71000,71278,71277,71303,71304,71582,71581,71607,71608,71886,71885,71911,71912,72190,72189,72215,72216,72799,73103,72494,72493,72822,73126,72519,72520,72799,72798,72822,72823,73408,73712,73103,73102,73429,73733,73126,73127,73408,73407,73429,73430,74017,74321,73712,73711,74036,74340,73733,73734,74322,74626,74017,74016,74339,74643,74036,74037,74627,74931,74322,74321,74628,74932,74641,74945,74642,74946,74339,74340,74933,75237,74628,74627,74934,75238,74943,75247,74944,75248,74641,74642,75239,75543,74934,74933,75240,75544,75241,75545,75242,75546,75243,75547,75244,75548,75245,75549,75246,75550,74943,74944]
		icepole = [67943,67944,67945,67946,67947,67948,67949,67950,68245,68246,68247,68248,68249,68250,68251,68252,68253,68254,68255,68256,68547,68548,68549,68550,68551,68552,68553,68554,68555,68556,68557,68558,68559,68560,68561,68562,68850,68851,68852,68853,68854,68855,68856,68857,68858,68859,68860,68861,68862,68863,68864,68865,68866,68867,69153,69154,69155,69156,69157,69158,69159,69160,69161,69162,69163,69164,69165,69166,69167,69168,69169,69170,69171,69172,69457,69458,69459,69460,69461,69462,69463,69464,69465,69466,69467,69468,69469,69470,69471,69472,69473,69474,69475,69476,69760,69761,69762,69763,69764,69765,69766,69767,69768,69769,69770,69771,69772,69773,69774,69775,69776,69777,69778,69779,69780,69781,70064,70065,70066,70067,70068,70069,70070,70071,70072,70073,70074,70075,70076,70077,70078,70079,70080,70081,70082,70083,70084,70085,70367,70368,70369,70370,70371,70372,70373,70374,70375,70376,70377,70378,70379,70380,70381,70382,70383,70384,70385,70386,70387,70388,70389,70390,70671,70672,70673,70674,70675,70676,70677,70678,70679,70680,70681,70682,70683,70684,70685,70686,70687,70688,70689,70690,70691,70692,70693,70694,70975,70976,70977,70978,70979,70980,70981,70982,70983,70984,70985,70986,70987,70988,70989,70990,70991,70992,70993,70994,70995,70996,70997,70998,71279,71280,71281,71282,71283,71284,71285,71286,71287,71288,71289,71290,71291,71292,71293,71294,71295,71296,71297,71298,71299,71300,71301,71302,71583,71584,71585,71586,71587,71588,71589,71590,71591,71592,71593,71594,71595,71596,71597,71598,71599,71600,71601,71602,71603,71604,71605,71606,71887,71888,71889,71890,71891,71892,71893,71894,71895,71896,71897,71898,71899,71900,71901,71902,71903,71904,71905,71906,71907,71908,71909,71910,72191,72192,72193,72194,72195,72196,72197,72198,72199,72200,72201,72202,72203,72204,72205,72206,72207,72208,72209,72210,72211,72212,72213,72214,72495,72496,72497,72498,72499,72500,72501,72502,72503,72504,72505,72506,72507,72508,72509,72510,72511,72512,72513,72514,72515,72516,72517,72518,72800,72801,72802,72803,72804,72805,72806,72807,72808,72809,72810,72811,72812,72813,72814,72815,72816,72817,72818,72819,72820,72821,73104,73105,73106,73107,73108,73109,73110,73111,73112,73113,73114,73115,73116,73117,73118,73119,73120,73121,73122,73123,73124,73125,73409,73410,73411,73412,73413,73414,73415,73416,73417,73418,73419,73420,73421,73422,73423,73424,73425,73426,73427,73428,73713,73714,73715,73716,73717,73718,73719,73720,73721,73722,73723,73724,73725,73726,73727,73728,73729,73730,73731,73732,74018,74019,74020,74021,74022,74023,74024,74025,74026,74027,74028,74029,74030,74031,74032,74033,74034,74035,74323,74324,74325,74326,74327,74328,74329,74330,74331,74332,74333,74334,74335,74336,74337,74338,74629,74630,74631,74632,74633,74634,74635,74636,74637,74638,74639,74640,74935,74936,74937,74938,74939,74940,74941,74942,]
		icepolecon = 0
		
		
		for val in range(0,len(icepoleedge),1):
			icepolecon = icepolecon+ice[icepoleedge[val]] /len(icepoleedge)
		
		for val2 in range(0,len(icepole),1):
			ice[icepole[val2]] = icepolecon	
		
		#for val3 in range(0,len(icepoleedge),1):
		#	ice[icepoleedge[val3]] = 100
		
		day = day+1
		count = count+1
		if day==32 and (month==1 or 3 or 5 or 7 or 8 or 10 or 12):
			day=1
			month = month+1
		elif day==31 and (month==4 or month==6 or month==9 or month==11):
			day=1
			month = month+1
		elif day==30 and month==2:
			day=1
			month = month+1
		try:
			with open(filename, 'wb') as frr:
				icewr = frr.write(ice)
		except:
			print('cant write')
	print('Done')
 

looop()
	