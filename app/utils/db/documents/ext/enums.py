from enum import Enum

class TTSMode(Enum):
	def __str__(self) -> str:
		return self.name

	never = 0
	only_when_muted = 1
	always = 2

class TTSVoices(Enum):
	def __str__(self) -> str:
		return self.name

	af_ZA_Standard_A = 0
	ar_XA_Standard_A = 1
	ar_XA_Standard_B = 2
	ar_XA_Standard_C = 3
	ar_XA_Standard_D = 4
	ar_XA_Wavenet_A = 5
	ar_XA_Wavenet_B = 6
	ar_XA_Wavenet_C = 7
	ar_XA_Wavenet_D = 8
	bg_BG_Standard_A = 9
	bn_IN_Standard_A = 10
	bn_IN_Standard_B = 11
	bn_IN_Wavenet_A = 12
	bn_IN_Wavenet_B = 13
	ca_ES_Standard_A = 14
	cmn_CN_Standard_A = 15
	cmn_CN_Standard_B = 16
	cmn_CN_Standard_C = 17
	cmn_CN_Standard_D = 18
	cmn_CN_Wavenet_A = 19
	cmn_CN_Wavenet_B = 20
	cmn_CN_Wavenet_C = 21
	cmn_CN_Wavenet_D = 22
	cmn_TW_Standard_A = 23
	cmn_TW_Standard_B = 24
	cmn_TW_Standard_C = 25
	cmn_TW_Wavenet_A = 26
	cmn_TW_Wavenet_B = 27
	cmn_TW_Wavenet_C = 28
	cs_CZ_Standard_A = 29
	cs_CZ_Wavenet_A = 30
	da_DK_Standard_A = 31
	da_DK_Standard_C = 32
	da_DK_Standard_D = 33
	da_DK_Standard_E = 34
	da_DK_Wavenet_A = 35
	da_DK_Wavenet_C = 36
	da_DK_Wavenet_D = 37
	da_DK_Wavenet_E = 38
	de_DE_Neural2_D = 39
	de_DE_Neural2_F = 40
	de_DE_Standard_A = 41
	de_DE_Standard_B = 42
	de_DE_Standard_C = 43
	de_DE_Standard_D = 44
	de_DE_Standard_E = 45
	de_DE_Standard_F = 46
	de_DE_Wavenet_A = 47
	de_DE_Wavenet_B = 48
	de_DE_Wavenet_C = 49
	de_DE_Wavenet_D = 50
	de_DE_Wavenet_E = 51
	de_DE_Wavenet_F = 52
	el_GR_Standard_A = 53
	el_GR_Wavenet_A = 54
	en_AU_Neural2_A = 55
	en_AU_Neural2_B = 56
	en_AU_Neural2_C = 57
	en_AU_Neural2_D = 58
	en_AU_News_E = 59
	en_AU_News_F = 60
	en_AU_News_G = 61
	en_AU_Standard_A = 62
	en_AU_Standard_B = 63
	en_AU_Standard_C = 64
	en_AU_Standard_D = 65
	en_AU_Wavenet_A = 66
	en_AU_Wavenet_B = 67
	en_AU_Wavenet_C = 68
	en_AU_Wavenet_D = 69
	en_GB_Neural2_A = 70
	en_GB_Neural2_B = 71
	en_GB_Neural2_C = 72
	en_GB_Neural2_D = 73
	en_GB_Neural2_F = 74
	en_GB_News_G = 75
	en_GB_News_H = 76
	en_GB_News_I = 77
	en_GB_News_J = 78
	en_GB_News_K = 79
	en_GB_News_L = 80
	en_GB_News_M = 81
	en_GB_Standard_A = 82
	en_GB_Standard_B = 83
	en_GB_Standard_C = 84
	en_GB_Standard_D = 85
	en_GB_Standard_F = 86
	en_GB_Wavenet_A = 87
	en_GB_Wavenet_B = 88
	en_GB_Wavenet_C = 89
	en_GB_Wavenet_D = 90
	en_GB_Wavenet_F = 91
	en_IN_Standard_A = 92
	en_IN_Standard_B = 93
	en_IN_Standard_C = 94
	en_IN_Standard_D = 95
	en_IN_Wavenet_A = 96
	en_IN_Wavenet_B = 97
	en_IN_Wavenet_C = 98
	en_IN_Wavenet_D = 99
	en_US_Neural2_A = 100
	en_US_Neural2_C = 101
	en_US_Neural2_D = 102
	en_US_Neural2_E = 103
	en_US_Neural2_F = 104
	en_US_Neural2_G = 105
	en_US_Neural2_H = 106
	en_US_Neural2_I = 107
	en_US_Neural2_J = 108
	en_US_News_K = 109
	en_US_News_L = 110
	en_US_News_M = 111
	en_US_News_N = 112
	en_US_Standard_A = 113
	en_US_Standard_B = 114
	en_US_Standard_C = 115
	en_US_Standard_D = 116
	en_US_Standard_E = 117
	en_US_Standard_F = 118
	en_US_Standard_G = 119
	en_US_Standard_H = 120
	en_US_Standard_I = 121
	en_US_Standard_J = 122
	en_US_Wavenet_A = 123
	en_US_Wavenet_B = 124
	en_US_Wavenet_C = 125
	en_US_Wavenet_D = 126
	en_US_Wavenet_E = 127
	en_US_Wavenet_F = 128
	en_US_Wavenet_G = 129
	en_US_Wavenet_H = 130
	en_US_Wavenet_I = 131
	en_US_Wavenet_J = 132
	es_ES_Neural2_A = 133
	es_ES_Neural2_B = 134
	es_ES_Neural2_C = 135
	es_ES_Neural2_D = 136
	es_ES_Neural2_E = 137
	es_ES_Neural2_F = 138
	es_ES_Standard_A = 139
	es_ES_Standard_B = 140
	es_ES_Standard_C = 141
	es_ES_Standard_D = 142
	es_ES_Wavenet_B = 143
	es_ES_Wavenet_C = 144
	es_ES_Wavenet_D = 145
	es_US_Neural2_A = 146
	es_US_Neural2_B = 147
	es_US_Neural2_C = 148
	es_US_News_D = 149
	es_US_News_E = 150
	es_US_News_F = 151
	es_US_News_G = 152
	es_US_Standard_A = 153
	es_US_Standard_B = 154
	es_US_Standard_C = 155
	es_US_Wavenet_A = 156
	es_US_Wavenet_B = 157
	es_US_Wavenet_C = 158
	fi_FI_Standard_A = 159
	fi_FI_Wavenet_A = 160
	fil_PH_Standard_A = 161
	fil_PH_Standard_B = 162
	fil_PH_Standard_C = 163
	fil_PH_Standard_D = 164
	fil_PH_Wavenet_A = 165
	fil_PH_Wavenet_B = 166
	fil_PH_Wavenet_C = 167
	fil_PH_Wavenet_D = 168
	fr_CA_Neural2_A = 169
	fr_CA_Neural2_B = 170
	fr_CA_Standard_A = 171
	fr_CA_Standard_B = 172
	fr_CA_Standard_C = 173
	fr_CA_Standard_D = 174
	fr_CA_Wavenet_A = 175
	fr_CA_Wavenet_B = 176
	fr_CA_Wavenet_C = 177
	fr_CA_Wavenet_D = 178
	fr_FR_Neural2_A = 179
	fr_FR_Neural2_B = 180
	fr_FR_Neural2_C = 181
	fr_FR_Neural2_D = 182
	fr_FR_Neural2_E = 183
	fr_FR_Standard_A = 184
	fr_FR_Standard_B = 185
	fr_FR_Standard_C = 186
	fr_FR_Standard_D = 187
	fr_FR_Standard_E = 188
	fr_FR_Wavenet_A = 189
	fr_FR_Wavenet_B = 190
	fr_FR_Wavenet_C = 191
	fr_FR_Wavenet_D = 192
	fr_FR_Wavenet_E = 193
	gu_IN_Standard_A = 194
	gu_IN_Standard_B = 195
	gu_IN_Wavenet_A = 196
	gu_IN_Wavenet_B = 197
	hi_IN_Standard_A = 198
	hi_IN_Standard_B = 199
	hi_IN_Standard_C = 200
	hi_IN_Standard_D = 201
	hi_IN_Wavenet_A = 202
	hi_IN_Wavenet_B = 203
	hi_IN_Wavenet_C = 204
	hi_IN_Wavenet_D = 205
	hu_HU_Standard_A = 206
	hu_HU_Wavenet_A = 207
	id_ID_Standard_A = 208
	id_ID_Standard_B = 209
	id_ID_Standard_C = 210
	id_ID_Standard_D = 211
	id_ID_Wavenet_A = 212
	id_ID_Wavenet_B = 213
	id_ID_Wavenet_C = 214
	id_ID_Wavenet_D = 215
	is_IS_Standard_A = 216
	it_IT_Neural2_A = 217
	it_IT_Neural2_C = 218
	it_IT_Standard_A = 219
	it_IT_Standard_B = 220
	it_IT_Standard_C = 221
	it_IT_Standard_D = 222
	it_IT_Wavenet_A = 223
	it_IT_Wavenet_B = 224
	it_IT_Wavenet_C = 225
	it_IT_Wavenet_D = 226
	ja_JP_Neural2_B = 227
	ja_JP_Neural2_C = 228
	ja_JP_Neural2_D = 229
	ja_JP_Standard_A = 230
	ja_JP_Standard_B = 231
	ja_JP_Standard_C = 232
	ja_JP_Standard_D = 233
	ja_JP_Wavenet_A = 234
	ja_JP_Wavenet_B = 235
	ja_JP_Wavenet_C = 236
	ja_JP_Wavenet_D = 237
	kn_IN_Standard_A = 238
	kn_IN_Standard_B = 239
	kn_IN_Wavenet_A = 240
	kn_IN_Wavenet_B = 241
	ko_KR_Standard_A = 242
	ko_KR_Standard_B = 243
	ko_KR_Standard_C = 244
	ko_KR_Standard_D = 245
	ko_KR_Wavenet_A = 246
	ko_KR_Wavenet_B = 247
	ko_KR_Wavenet_C = 248
	ko_KR_Wavenet_D = 249
	lv_LV_Standard_A = 250
	ml_IN_Standard_A = 251
	ml_IN_Standard_B = 252
	ml_IN_Wavenet_A = 253
	ml_IN_Wavenet_B = 254
	ml_IN_Wavenet_C = 255
	ml_IN_Wavenet_D = 256
	mr_IN_Standard_A = 257
	mr_IN_Standard_B = 258
	mr_IN_Standard_C = 259
	mr_IN_Wavenet_A = 260
	mr_IN_Wavenet_B = 261
	mr_IN_Wavenet_C = 262
	ms_MY_Standard_A = 263
	ms_MY_Standard_B = 264
	ms_MY_Standard_C = 265
	ms_MY_Standard_D = 266
	ms_MY_Wavenet_A = 267
	ms_MY_Wavenet_B = 268
	ms_MY_Wavenet_C = 269
	ms_MY_Wavenet_D = 270
	nb_NO_Standard_A = 271
	nb_NO_Standard_B = 272
	nb_NO_Standard_C = 273
	nb_NO_Standard_D = 274
	nb_NO_Standard_E = 275
	nb_NO_Wavenet_A = 276
	nb_NO_Wavenet_B = 277
	nb_NO_Wavenet_C = 278
	nb_NO_Wavenet_D = 279
	nb_NO_Wavenet_E = 280
	nl_BE_Standard_A = 281
	nl_BE_Standard_B = 282
	nl_BE_Wavenet_A = 283
	nl_BE_Wavenet_B = 284
	nl_NL_Standard_A = 285
	nl_NL_Standard_B = 286
	nl_NL_Standard_C = 287
	nl_NL_Standard_D = 288
	nl_NL_Standard_E = 289
	nl_NL_Wavenet_A = 290
	nl_NL_Wavenet_B = 291
	nl_NL_Wavenet_C = 292
	nl_NL_Wavenet_D = 293
	nl_NL_Wavenet_E = 294
	pa_IN_Standard_A = 295
	pa_IN_Standard_B = 296
	pa_IN_Standard_C = 297
	pa_IN_Standard_D = 298
	pa_IN_Wavenet_A = 299
	pa_IN_Wavenet_B = 300
	pa_IN_Wavenet_C = 301
	pa_IN_Wavenet_D = 302
	pl_PL_Standard_A = 303
	pl_PL_Standard_B = 304
	pl_PL_Standard_C = 305
	pl_PL_Standard_D = 306
	pl_PL_Standard_E = 307
	pl_PL_Wavenet_A = 308
	pl_PL_Wavenet_B = 309
	pl_PL_Wavenet_C = 310
	pl_PL_Wavenet_D = 311
	pl_PL_Wavenet_E = 312
	pt_BR_Neural2_A = 313
	pt_BR_Neural2_B = 314
	pt_BR_Neural2_C = 315
	pt_BR_Standard_A = 316
	pt_BR_Standard_B = 317
	pt_BR_Standard_C = 318
	pt_BR_Wavenet_A = 319
	pt_BR_Wavenet_B = 320
	pt_BR_Wavenet_C = 321
	pt_PT_Standard_A = 322
	pt_PT_Standard_B = 323
	pt_PT_Standard_C = 324
	pt_PT_Standard_D = 325
	pt_PT_Wavenet_A = 326
	pt_PT_Wavenet_B = 327
	pt_PT_Wavenet_C = 328
	pt_PT_Wavenet_D = 329
	ro_RO_Standard_A = 330
	ro_RO_Wavenet_A = 331
	ru_RU_Standard_A = 332
	ru_RU_Standard_B = 333
	ru_RU_Standard_C = 334
	ru_RU_Standard_D = 335
	ru_RU_Standard_E = 336
	ru_RU_Wavenet_A = 337
	ru_RU_Wavenet_B = 338
	ru_RU_Wavenet_C = 339
	ru_RU_Wavenet_D = 340
	ru_RU_Wavenet_E = 341
	sk_SK_Standard_A = 342
	sk_SK_Wavenet_A = 343
	sr_rs_Standard_A = 344
	sv_SE_Standard_A = 345
	sv_SE_Standard_B = 346
	sv_SE_Standard_C = 347
	sv_SE_Standard_D = 348
	sv_SE_Standard_E = 349
	sv_SE_Wavenet_A = 350
	sv_SE_Wavenet_B = 351
	sv_SE_Wavenet_C = 352
	sv_SE_Wavenet_D = 353
	sv_SE_Wavenet_E = 354
	ta_IN_Standard_A = 355
	ta_IN_Standard_B = 356
	ta_IN_Standard_C = 357
	ta_IN_Standard_D = 358
	ta_IN_Wavenet_A = 359
	ta_IN_Wavenet_B = 360
	ta_IN_Wavenet_C = 361
	ta_IN_Wavenet_D = 362
	te_IN_Standard_A = 363
	te_IN_Standard_B = 364
	th_TH_Standard_A = 365
	tr_TR_Standard_A = 366
	tr_TR_Standard_B = 367
	tr_TR_Standard_C = 368
	tr_TR_Standard_D = 369
	tr_TR_Standard_E = 370
	tr_TR_Wavenet_A = 371
	tr_TR_Wavenet_B = 372
	tr_TR_Wavenet_C = 373
	tr_TR_Wavenet_D = 374
	tr_TR_Wavenet_E = 375
	uk_UA_Standard_A = 376
	uk_UA_Wavenet_A = 377
	vi_VN_Standard_A = 378
	vi_VN_Standard_B = 379
	vi_VN_Standard_C = 380
	vi_VN_Standard_D = 381
	vi_VN_Wavenet_A = 382
	vi_VN_Wavenet_B = 383
	vi_VN_Wavenet_C = 384
	vi_VN_Wavenet_D = 385
	yue_HK_Standard_A = 386
	yue_HK_Standard_B = 387
	yue_HK_Standard_C = 388
	yue_HK_Standard_D = 389

class TWBFMode(Enum):
	def __str__(self) -> str:
		return self.name

	true = 0
	whitelist = 1
	blacklist = 2
	false = 3

class AUCooldownMode(Enum):
	def __str__(self) -> str:
		return self.name

	none = 0
	user = 1
	channel = 2
	guild = 3

class AutoResponseMethod(Enum):
	def __str__(self) -> str:
		return self.name

	exact = 0
	contains = 1
	regex = 2 # different from data.regex, this method uses raw matching rather than adding filtering
	mention = 3

class AutoResponseType(Enum):
	def __str__(self) -> str:
		return self.name

	text = 0
	file = 1
	script = 2