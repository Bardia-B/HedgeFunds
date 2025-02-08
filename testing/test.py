def clean_and_save_hedge_funds():
    # The raw data as a multi-line string (your provided data)
    raw_data = """BERKSHIRE HATHAWAY INC	Warren Buffett
2	Scion Asset Management, LLC	Michael Burry
3	BlackRock Inc.	
4	RENAISSANCE TECHNOLOGIES LLC	James Simons
5	BAKER BROS. ADVISORS LP	Julian and Felix Baker
6	CITADEL ADVISORS LLC	Ken Griffin
7	Bridgewater Associates, LP	Ray Dalio, Bob Prince
8	VANGUARD GROUP INC	
9	SABBY MANAGEMENT, LLC	Hal David Mintz
10	PERCEPTIVE ADVISORS LLC	Joseph Edelman
11	Point72 Asset Management, L.P.	Steven Cohen
12	BAUPOST GROUP LLC/MA	Seth Klarman
13	ARK Investment Management LLC	Catherine Wood
14	SUSQUEHANNA INTERNATIONAL GROUP, LLP	
15	Pershing Square Capital Management, L.P.	Bill Ackman
16	MORGAN STANLEY	
17	GOLDMAN SACHS GROUP INC	
18	TIGER GLOBAL MANAGEMENT LLC	Chase Coleman, Feroz Dewan
19	ARMISTICE CAPITAL, LLC	Steven Boyd
20	Duquesne Family Office LLC	Stanley Druckenmiller
21	RA CAPITAL MANAGEMENT, L.P.	Peter Kolchinsky
22	FMR LLC	
23	JPMORGAN CHASE & CO	
24	SOROS FUND MANAGEMENT LLC	George Soros
25	Third Point LLC	Dan Loeb
26	Melvin Capital Management LP	Gabriel Plotkin
27	BAILLIE GIFFORD & CO	
28	ORBIMED ADVISORS LLC	Samuel Isaly
29	JANE STREET GROUP, LLC	
30	MILLENNIUM MANAGEMENT LLC	Israel Englander
31	ICAHN CARL C	Carl Icahn
32	INTRACOASTAL CAPITAL, LLC	Mitchell Kopin and Daniel Asher
33	GREENLIGHT CAPITAL INC	David Einhorn
34	CVI Investments, Inc.	
35	BIOTECHNOLOGY VALUE FUND L P	Mark N. Lampert
36	Empery Asset Management, LP	Ryan Matthew Lane and Martin David Hoe
37	STATE STREET CORP	
38	EcoR1 Capital, LLC	
39	Ark Investment Management Llc	
40	Hudson Bay Capital Management LP	
41	Starboard Value LP	Jeffrey Smith
42	BANK OF AMERICA CORP /DE/	
43	Gotham Asset Management, LLC	Joel Greenblatt
44	Ark ETF Trust - ARK Innovation ETF	
45	TWO SIGMA INVESTMENTS, LP	John Overdeck, David Siegel
46	Blackstone Alternative Investment Funds - Blackstone Alternative Multi-Strategy Fund Class I	
47	Himalaya Capital Management LLC	Li Lu
48	CASCADE INVESTMENT, L.L.C.	William Gates and Michael Larson
49	GAMCO INVESTORS, INC. ET AL	Mario Gabelli
50	Avoro Capital Advisors LLC	
51	LONE PINE CAPITAL LLC	Stephen Mandel
52	COATUE MANAGEMENT LLC	
53	VANGUARD INDEX FUNDS - Vanguard Total Stock Market Index Fund Investor Shares	
54	Redmile Group, LLC	
55	APPALOOSA MANAGEMENT LP	David Tepper
56	OAKTREE CAPITAL MANAGEMENT LP	Howard Marks
57	Opaleye Management Inc.	
58	Dalal Street, LLC	Mohnish Pabrai
59	TUDOR INVESTMENT CORP ET AL	Paul Tudor Jones
60	HILLHOUSE CAPITAL MANAGEMENT, LTD.	
61	Whale Rock Capital Management LLC	
62	Altimeter Capital Management, LP	
63	VIKING GLOBAL INVESTORS LP	Andreas Halvorsen, David Ott
64	GEODE CAPITAL MANAGEMENT, LLC	
65	RC Ventures LLC	
66	PRICE T ROWE ASSOCIATES INC /MD/	
67	SIMPLEX TRADING, LLC	
68	Abdiel Capital Advisors, LP	
69	Altium Capital Management LP	
70	D. E. Shaw & Co., Inc.	DE Shaw
71	Sarissa Capital Management LP	
72	RTW INVESTMENTS, LP	
73	Boxer Capital, LLC	
74	BILL & MELINDA GATES FOUNDATION TRUST	
75	AQR CAPITAL MANAGEMENT LLC	Cliff Asness
76	WELLINGTON MANAGEMENT GROUP LLP	
77	Virtu Financial LLC	
78	APPALOOSA LP	
79	Tencent Holdings Ltd	
80	Cormorant Asset Management, LP	
81	Elliott Investment Management L.P.	Paul Singer
82	UBS ASSET MANAGEMENT AMERICAS INC	
83	BVF INC/IL	
84	AKRE CAPITAL MANAGEMENT LLC	
85	Saba Capital Management, L.P.	Boaz Ronald Weinstein
86	Cutler Group LP	
87	Elliott Management Corporation	
88	NEA Management Company, LLC	
89	Casdin Capital, LLC	
90	Anson Funds Management LP	Bruce Winson
91	DEERFIELD MANAGEMENT COMPANY, L.P. (SERIES C)	
92	DIMENSIONAL FUND ADVISORS LP	
93	Fisher Asset Management, LLC	
94	PUBLIC INVESTMENT FUND	
95	CITADEL SECURITIES LLC	
96	Fundsmith LLP	Terry Smith
97	BLACKROCK FUNDS - BLACKROCK EXCHANGE PORTFOLIO BLACKROCK	
98	BIGGER CAPITAL FUND L P	
99	AWM Investment Company, Inc.	
100	VANGUARD INDEX FUNDS - Vanguard Extended Market Index Fund Investor Shares	
101	HILLHOUSE CAPITAL ADVISORS, LTD.	
102	ADAGE CAPITAL PARTNERS GP, L.L.C.	Phil Gross, Robert Atchinson
103	WOLVERINE TRADING, LLC	
104	PAULSON & CO. INC.	John Paulson
105	TCI Fund Management Ltd	
106	Capital World Investors	
107	UBS Group AG	
108	GREAT POINT PARTNERS LLC	
109	GROUP ONE TRADING, L.P.	
110	WELLS FARGO & COMPANY/MN	
111	Temasek Holdings (Private) Ltd	
112	Broadfin Capital, LLC	
113	Elliott Associates, L.P.	
114	Invesco Ltd.	
115	TWO SIGMA ADVISERS, LP	
116	Ark ETF Trust - ARK Genomic Revolution ETF	
117	CITIGROUP INC	
118	Man Group plc	
119	Consonance Capital Management LP	
120	Iroquois Capital Management, LLC	
121	DEUTSCHE BANK AG\	
122	ValueAct Holdings, L.P.	Jeff Ubben
123	TWO SIGMA SECURITIES, LLC	
124	Blackstone Group Inc	
125	Ikarian Capital, LLC	
126	Ark ETF Trust - ARK Next Generation Internet ETF	
127	NORTHERN TRUST CORP	
128	CHARLES SCHWAB INVESTMENT MANAGEMENT INC	
129	Point72 Hong Kong Ltd	Steven Cohen
130	Bridgewater Advisors Inc.	
131	ROTHSCHILD INVESTMENT CORP /IL	
132	Swiss National Bank	
133	BARCLAYS PLC	
134	D. E. SHAW & CO, L.P.	DE Shaw
135	ROYAL BANK OF CANADA	
136	Rockefeller Capital Management L.P.	
137	BlackRock, Inc.	
138	Senvest Management, LLC	
139	TANG CAPITAL MANAGEMENT LLC	
140	Capital Research Global Investors	
141	JANA PARTNERS LLC	
142	Kynikos Associates LP	James S. "Jim" Chanos
143	Venrock Healthcare Capital Partners II, L.P.	
144	Nantahala Capital Management, LLC	
145	Deep Track Capital, LP	
146	SANDS CAPITAL MANAGEMENT, LLC	
147	ALKEON CAPITAL MANAGEMENT LLC	
148	TANG CAPITAL PARTNERS LP	
149	Bank of New York Mellon Corp	
150	Vivo Capital, LLC	
151	Dorsey Asset Management, LLC	
152	JENNISON ASSOCIATES LLC	
153	Bill & Melinda Gates Foundation	
154	HIRSCHMAN ORIN	
155	SOFTBANK GROUP CORP	
156	Silver Lake Group, L.L.C.	
157	Dragoneer Investment Group, LLC	
158	LIGHT STREET CAPITAL MANAGEMENT, LLC	
159	BB BIOTECH AG	
160	CANADA PENSION PLAN INVESTMENT BOARD	
161	FARALLON CAPITAL MANAGEMENT LLC	Thomas Steyer
162	DAFNA Capital Management LLC	
163	ABRAMS CAPITAL MANAGEMENT, L.P.	
164	MAVERICK CAPITAL LTD	
165	FRANKLIN RESOURCES INC	
166	TRIAN FUND MANAGEMENT, L.P.	
167	IFP Advisors, Inc	
168	Flynn James E	
169	NORGES BANK	
170	Parallax Volatility Advisers, L.P.	
171	Matrix Capital Management Company, LP	David Goel
172	Stonepine Capital Management, LLC	
173	RA Capital Healthcare Fund LP	
174	CREDIT SUISSE AG/	
175	Select Equity Group, L.P.	
176	Ark ETF Trust - ARK Autonomous Technology & Robotics ETF	
177	Night Owl Capital Management, LLC	
178	Sumitomo Mitsui Trust Holdings, Inc.	
179	CTC LLC	
180	Palo Alto Investors LP	
181	Proequities, Inc.	
182	iSHARES TRUST - iShares Russell 2000 ETF	
183	BROOKFIELD ASSET MANAGEMENT INC.	Bruce Flatt
184	L1 Capital Global Opportunities Master Fund, Ltd.	
185	CALIFORNIA PUBLIC EMPLOYEES RETIREMENT SYSTEM	
186	Gamestop Corp.	
187	683 Capital Management, LLC	
188	cobas asset management, sgiic, s.a.	
189	Aquamarine Capital Management, LLC	
190	BNP PARIBAS ARBITRAGE, SA	
191	DODGE & COX	
192	SCGE MANAGEMENT, L.P.	
193	BlueCrest Capital Management Ltd	Michael Platt
194	D1 Capital Partners L.P.	Daniel Sundheim
195	Rock Springs Capital Management LP	
196	GLENVIEW CAPITAL MANAGEMENT, LLC	
197	Sculptor Capital LP	Daniel Och
198	Arlington Value Capital, LLC	
199	Jefferies Group LLC	
200	Musk Elon	
201	Long Pond Capital, LP	John Khoury
202	IMC-Chicago, LLC	
203	CAS Investment Partners, LLC	
204	BlackRock Investment Management, LLC	
205	BlackRock Fund Advisors	
206	PERISCOPE CAPITAL INC.	
207	SUSQUEHANNA SECURITIES, LLC	
208	Turtle Creek Asset Management Inc.	
209	CALIFORNIA STATE TEACHERS RETIREMENT SYSTEM	
210	VANGUARD INSTITUTIONAL INDEX FUNDS - Vanguard Institutional Total Stock Market Index Fund Institutional Shares	
211	Logos Global Management LP	
212	GLAZER CAPITAL, LLC	
213	BANK OF MONTREAL /CAN/	
214	PEAK6 Investments LLC	
215	Corvex Management LP	Keith Meister
216	Citadel Securities GP LLC	
217	Lincoln Park Capital Fund, LLC	
218	ALLIANCEBERNSTEIN L.P.	
219	SRS Investment Management, LLC	
220	SUVRETTA CAPITAL MANAGEMENT, LLC	
221	ADW Capital Partners, L.P.	Adam Wyden
222	Grantham, Mayo, Van Otterloo & Co. LLC	
223	Sio Capital Management, LLC	
224	PRIMECAP MANAGEMENT CO/CA/	
225	AMAZON COM INC	
226	Fundsmith Equity Fund, L.p.	
227	EMINENCE CAPITAL, LP	
228	RAYMOND JAMES & ASSOCIATES	
229	Magnetar Financial LLC	
230	Capital International Investors	
231	Abdiel Qualified Master Fund LP	
232	Novo Holdings A/S	
233	BUFFETT WARREN E	
234	NOMURA HOLDINGS INC	
235	Esousa Holdings LLC	
236	ARROWSTREET CAPITAL, LIMITED PARTNERSHIP	
237	ROYCE & ASSOCIATES LP	Chuck Royce
238	GIC Private Ltd	
239	Rubric Capital Management LP	
240	MARKEL CORP	
241	Citadel Advisors Holdings Lp	
242	BALYASNY ASSET MANAGEMENT LLC	
243	Polar Asset Management Partners Inc.	
244	iSHARES TRUST - iShares Core S&P 500 ETF	
245	FAIRFAX FINANCIAL HOLDINGS LTD/ CAN	
246	DAVIDSON KEMPNER CAPITAL MANAGEMENT LP	Thomas Kempner, Marvin Davidson
247	Ault Global Holdings, Inc.	
248	LYTTON LAURENCE W	
249	Bain Capital Life Sciences Investors, LLC	
250	GOLDMAN SACHS ASSET MANAGEMENT, L.P.
    """
    
    # Split the data into lines and process each line
    hedge_funds = []
    
    # Split the raw data into lines
    lines = raw_data.strip().split('\n')
    
    # Process each line
    for line in lines:
        # Split by tab and get just the fund name (second column)
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            fund_name = parts[1].strip()
            # Clean up the fund name
            fund_name = fund_name.replace('"', '')  # Remove quotes
            hedge_funds.append(fund_name)
    
    # Write to file
    with open('hedge_fund_names.txt', 'w') as f:
        for fund in hedge_funds:
            f.write(fund + '\n')
    
    print(f"Successfully saved {len(hedge_funds)} hedge fund names to 'hedge_fund_names.txt'")

# Run the function
clean_and_save_hedge_funds()