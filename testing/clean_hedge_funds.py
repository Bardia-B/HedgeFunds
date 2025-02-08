def clean_hedge_fund_data(raw_data):
    """Clean hedge fund data and extract only the names"""
    # Split the data into lines
    lines = raw_data.strip().split('\n')
    
    # Extract just the fund names (second column after splitting by tabs)
    hedge_funds = []
    for line in lines:
        # Skip empty lines and the header/footer
        if not line.strip() or 'Rank' in line or 'AUM' in line:
            continue
            
        # Split by tab and get the fund name (second column)
        parts = line.split('\t')
        if len(parts) >= 2:
            # Clean the fund name
            fund_name = parts[1].strip()
            # Remove location and AUM info if present
            fund_name = fund_name.split('\t')[0]
            hedge_funds.append(fund_name)
    
    return hedge_funds

def save_hedge_funds(hedge_funds, filename='clean_hedge_funds.txt'):
    """Save the cleaned hedge fund names to a file"""
    with open(filename, 'w') as f:
        for fund in hedge_funds:
            f.write(f"{fund}\n")

# Example hedge fund data (your long list goes here)
raw_data = """1	Field Street Capital Management	New York	$ 297,961	Credit, Global Macro
2	Citadel Investment Group	Chicago	$ 253,353	Convertibles, Multi Strategy
3	Bridgewater Associates	Westport	$ 235,542	Long/Short, Global Macro
4	Mariner Investment Group LLC	New York	$ 219,309	Arbitrage
5	Millennium Capital Partners	New York	$ 218,000	Multi Strategy
6	Ares Management	Los Angeles	$ 193,679	Managed Futures, Fixed Income
7	Balyasny Asset Management	Chicago	$ 180,959	Multi Strategy, Global Equity
8	AQR Capital Management	Greenwich	$ 145,451	Multi Strategy, Managed Futures
9	Point72 Asset Management	Stamford	$ 138,459	
10	Rokos Capital Management	London	$ 138,426	Global Macro
11	DE Shaw	New York	$ 128,024	Absolute Returns
12	Willis Towers Watson	London	$ 128,000	Fund of Funds
13	Tiger Global Management LLC	New York	$ 124,655	
14	Garda Capital	Minneapolis	$ 124,164	Global Macro, Event Driven
15	Renaissance Technologies	East Setauket	$ 121,849	Crypto, Multi Strategy
16	Capula Investment Management LLP	London	$ 118,360	Absolute Returns, Credit
17	Fortress Investment Group	New York	$ 114,347	Private Equity, Global Macro
18	Goldman Sachs Asset Management	New York	$ 106,240	Multi Strategy, Fund of Funds
19	Exoduspoint Capital Management, LP	New York	$ 86,211	Multi-Strategy
20	Two Sigma International Limited	London	$ 81,175	Long/Short
21	Two Sigma Investments	New York	$ 81,175	Commodities
22	Cerberus Capital Management	New York	$ 80,581	Credit, Real Estate
23	Squarepoint Ops	London	$ 75,717	Quantitative
24	Angelo Gordon & Co.	New York	$ 74,642	Real Estate, Fixed Income
25	Coatue Management	New York	$ 73,334	
26	Hillhouse Capital	Hong Kong	$ 70,707	Emerging Markets
27	Haidar Capital Management	New York	$ 62,551	Global Macro, Multi Strategy
28	Viking Global Investors	Greenwich	$ 59,833	Global Macro, Long/Short
29	Brevan Howard Asset Management	London	$ 58,630	Global Macro, Commodities
30	Select Equity	New York	$ 58,473	Equity, Long/Short
31	Adage Capital Management	Boston	$ 58,166	Global Equity
32	III Capital	Boca Raton	$ 57,116	Credit
33	Och-Ziff Capital Management	New York	$ 55,483	Global Macro, Convertibles
34	Sculptor Capital Management	New York	$ 55,483	Multi-Strategy, Real Estate
35	GoldenTree Asset Management	New York	$ 51,980	Credit, Absolute Returns
36	Lighthouse Investment Partners	Palm Beach Gardens	$ 51,918	Fund of Funds, Long/Short
37	Bracebridge Capital	Boston	$ 48,750	Absolute Returns, Commodities
38	Element Capital Management	New York	$ 48,491	Global Macro, Credit
39	Davidson Kempner Capital Management	New York	$ 44,058	Global Equity, Distressed Assets
40	Farallon Capital Management	San Francisco	$ 42,196	Multi Strategy, Arbitrage
41	Alphadyne Asset Management	New York	$ 39,266	Equity, Managed Futures
42	Tenaron Capital Management	New York	$ 39,153	Global Macro
43	Oaktree Capital Management	Los Angeles	$ 38,350	Fixed Income, Real Estate
44	Symmetry Investments	Hong Kong	$ 36,435	Credit
45	Lone Pine Capital	Greenwich	$ 35,538	Long/Short, Emerging Markets
46	HBK Capital Management	Dallas	$ 33,664	Multi Strategy
47	BlackRock Alternative Advisors	New York	$ 33,250	Global Macro, Convertibles
48	Apollo Capital	New York	$ 32,680	Managed Futures, Credit
49	Anchorage Capital Group	New York	$ 32,324	Credit, Event Driven
50	Lansdowne Partners	London	$ 31,740	Absolute Returns, Global Macro
51	Pictet Alternative Investments	Geneva	$ 31,715	Fund of Funds
52	Baupost Group	Boston	$ 31,606	Global Equity, Long/Short
53	Brigade Capital Management	New York	$ 31,001	Managed Futures, Distressed Assets
54	Centerbridge Partners LP	New York	$ 30,945	Multi Strategy, Distressed Assets
55	Polar Capital Partners	London	$ 30,348	Long/Short, Convertibles
56	Wafra Investment Group	New York	$ 30,220	Multi Strategy
57	Kayne Anderson Capital Advisors	Los Angeles	$ 29,824	Private Equity, Multi Strategy
58	Magnetar Capital	Evanston	$ 29,448	Multi Strategy, Managed Futures
59	Marshall Wace	London	$ 28,400	Global Macro, Multi Strategy
60	Polar Asset Management Partners	Toronto	$ 28,366	
61	Holocene Advisors	New York	$ 28,349	Long/Short
62	Cheyne Capital	London	$ 27,889	Real Estate, Fixed Income
63	Moore Capital Management	New York	$ 27,738	Global Macro, Emerging Markets
64	Third Point LLC	New York	$ 27,574	Event Driven, Activist
65	Benefit Street Partners	New York	$ 27,535	Credit
66	Voloridge Investment Management	Jupiter	$ 27,506	Quantitative
67	Wellington Management Company LLP	Boston	$ 27,210	Multi Strategy, Commodities
68	Lindsell Train Limited	London	$ 26,990	Fixed Income, Asian Equity
69	Capstone Investment Advisors LLC	New York	$ 26,990	Derivatives, Global Equity
70	Caxton Associates	New York	$ 26,687	Global Macro
71	Marathon Asset Management	New York	$ 26,228	Credit, Emerging Markets
72	UBS Hedge Fund Solutions	Stamford	$ 26,135	Equity
73	Man Group	London	$ 26,040	Global Macro, Convertibles
74	Shenkman Capital Management	New York	$ 25,067	Convertibles, Fixed Income
75	Tudor Investment Corporation	Stamford	$ 24,884	Crypto, Multi Strategy
76	King Street Capital Management	New York	$ 24,857	Global Macro, FX
77	Alkeon Capital Management	New York	$ 24,375	
78	Egerton Capital	London	$ 24,344	Long/Short
79	Lyxor Asset Management	Paris	$ 24,152	Convertibles, Long/Short
80	Alcentra	London	$ 22,590	Distressed Assets
81	TIG Advisors	New York	$ 22,140	Global Equity, Long/Short
82	Varde Partners	Minneapolis	$ 21,577	Distressed Assets, Event Driven
83	LaSalle Investment Management	Chicago	$ 21,440	Real Estate
84	Whale Rock Capital Management	Boston	$ 20,854	
85	Silver Point Capital	Greenwich	$ 20,631	Multi Strategy, Distressed Assets
86	BTG Pactual	Sao Paulo	$ 20,617	Emerging Markets
87	Nephila Capital	Larkspur	$ 20,447	Insurance, Commodities
88	Hudson Bay Capital Management	New York	$ 20,121	Multi Strategy
89	Crestline Investors	Fort Worth	$ 20,097	Fund of Funds, Event Driven
90	Strategic Value Partners	Greenwich	$ 19,897	Distressed Assets
91	Arrowstreet Capital	Boston	$ 19,600	Emerging Markets, Long/Short
92	Barings	London	$ 19,289	Fund of Funds, Multi Strategy
93	Appaloosa Management	Short Hills	$ 19,100	Global Equity, Fixed Income
94	Beach Point Capital Management	Santa Monica	$ 19,097	Multi Strategy, Credit
95	BFAM Partners	Hong Kong	$ 18,965	Multi-Strategy, Credit
96	Grantham, Mayo, Van Otterloo & Co.	Boston	$ 18,960	Emerging Markets, Global Macro
97	Systematica Investments	London	$ 18,629	Commodities
98	CarVal Investors	Minneapolis	$ 18,305	Fixed Income, Real Estate
99	Parallax Fund	San Francisco	$ 18,213	Multi Strategy
100	GAM Fund Management	Hong Kong	$ 18,033	Fund of Funds
101	Altimeter Capital	Boston	$ 17,950	Long/Short
102	Canyon Partners	Los Angeles	$ 17,892	Multi Strategy, Convertibles
103	Algebris Investments	London	$ 17,877	Credit, UCITS
104	Sprott Asset Management	Toronto	$ 17,868	Small Cap, Long/Short
105	OrbiMed Advisors	New York	$ 17,321	Private Equity
106	MJX Asset Management	New York	$ 17,314	CDO, Credit
107	Pershing Square Capital Management	New York	$ 16,798	Value, Activist
108	Perella Weinberg Partners	New York	$ 16,552	Event Driven
109	Pharo Management	New York	$ 16,368	Global Macro, Emerging Markets
110	Ardea Investment Management	Sydney, Nsw	$ 16,079	Fixed Income
111	Neuberger Berman	New York	$ 15,900	Fund of Funds, ESG
112	Rock Creek	Washington	$ 15,669	Multi Strategy, Fund of Funds
113	Cevian Capital	Stockholm	$ 15,646	Activist, Event Driven
114	Pacific Alternative Asset Management	Irvine	$ 15,583	Fund of Funds, Arbitrage
115	Universa Investments	Miami	$ 15,549	Quantitative
116	Danske Capital	Copenhagen	$ 15,500	European Equity, Fixed Income
117	Waterfall Asset Management	New York	$ 15,492	MBS, Credit
118	LMR Partners	London	$ 15,350	Global Macro, Event Driven
119	Onex Credit Partners	Toronto	$ 15,200	Credit
120	Rockpoint Group	Boston	$ 15,122	Real Estate
121	Knighthead Capital Management, LLC	New York	$ 14,734	Long/Short, Credit
122	Bayview Asset Management	Coral Gables	$ 14,700	Credit
123	Commonfund Capital	Wilton	$ 14,691	Multi Strategy, Fixed Income
124	Graham Capital Management	Rowayton	$ 14,653	Global Macro, Commodities
125	BlueMountain Capital	New York	$ 14,408	Long/Short, Credit
126	RWC London	London	$ 14,407	Absolute Returns, Long/Short
127	Brummer and Partners	Stockholm	$ 14,200	Long/Short, Multi Strategy
128	Lazard Alternatives	New York	$ 14,120	Multi Strategy, Real Estate
129	Laurion Capital Management	New York	$ 13,967	Multi Strategy
130	Soroban Capital Partners	New York	$ 13,722	Long/Short
131	Woodline Partners	San Francisco	$ 13,521	Long/Short
132	Entrust Permal	New York	$ 13,454	Fund of Funds, Long/Short
133	Diameter Capital Partners	New York	$ 13,360	Credit
134	ValueAct Capital	San Francisco	$ 13,233	Long/Short, Activist
135	MSD Capital	New York	$ 13,055	Credit, Global Macro
136	Paloma Partners	Greenwich	$ 12,944	Multi Strategy
137	Hildene Capital Management	Stamford	$ 12,924	Distressed Assets, Credit
138	PDT Partners	New York	$ 12,915	Quantitative
139	Maverick Capital	Dallas	$ 12,527	Global Macro, Multi Strategy
140	Samlyn Capital	New York	$ 12,509	
141	Platinum Asset Management	Sydney	$ 12,389	Equity
142	Janus Henderson	London	$ 12,231	Global Macro, Long/Short
143	Credit Suisse Alternatives	Zurich	$ 12,139	Fund of Funds
144	Napier Park Global Capital	New York	$ 11,677	Credit
145	Luxor Capital Group	New York	$ 11,490	Event Driven
146	Aristeia Capital	Greenwich	$ 11,417	Absolute Returns, Credit
147	Tennenbaum Capital Partners	Santa Monica	$ 11,354	Multi Strategy, Credit
148	Taconic Capital Advisors	New York	$ 11,140	Managed Futures, Multi Strategy
149	Steadfast Financial LP	New York	$ 11,134	Long/Short
150	Alyeska Investment Group	Chicago	$ 11,066	Managed Futures
151	Abrams Capital	Boston	$ 10,783	Managed Futures, Opportunistic
152	Wolverine Asset Management	Chicago	$ 10,762	Arbitrage
153	Whitebox Advisors	Minneapolis	$ 10,629	Global Macro, Convertibles
154	Eminence Capital	New York	$ 10,574	Activist
155	Ellington Management Group	Old Greenwich	$ 10,543	ABS, Credit
156	Aviva Investors	London	$ 10,510	Convertibles, Multi Strategy
157	Monarch Alternative Capital	New York	$ 10,446	Fixed Income, Distressed Assets
158	K2 Advisors	Stamford	$ 10,423	Fund of Funds
159	Corbin Capital Partners	New York	$ 10,362	Fund of Funds, Global Macro
160	ABC Arbitrage	Paris	$ 10,285	Arbitrage, Quantitative
161	EJF Asset Management	Arlington	$ 10,285	Event Driven, ABS
162	Altrinsic Global Advisors	Greenwich	$ 10,284	Equity
163	JP Morgan Alternative Investments	New York	$ 10,208	Multi Strategy, Fund of Funds
164	Pentwater Capital Management	Evanston	$ 9,864	Global Equity, Fixed Income
165	SPARX Group Co.	Tokyo	$ 9,809	Asian Equity
166	HG Vora Capital Management	New York	$ 9,744	Event Driven
167	Saba Capital	New York	$ 9,703	Credit
168	ArcLight Capital Partners	Boston	$ 9,599	Energy
169	Redwood Capital Management	Englewood Cliffs	$ 9,396	Credit
170	CSOP Asset Management	Hong Kong	$ 9,195	Credit, Emerging Markets
171	400 Capital Management LLC	New York	$ 9,115	Credit
172	Panagora	Boston	$ 9,110	Global Macro, Cannabis
173	Senator Investment Group	New York	$ 9,060	Long/Short
174	Transtrend	Rotterdam	$ 9,040	Managed Futures
175	BlueCrest Capital Management	London	$ 9,000	Multi Strategy, Managed Futures
176	LibreMax Capital	New York	$ 8,846	Distressed Assets, Credit
177	Natixis Alternative Investments	Boston	$ 8,690	Multi Strategy, Long/Short
178	Asia Frontier Capital	Hong Kong	$ 8,633	Emerging Markets
179	Libra Advisors	New York	$ 8,338	Long/Short
180	Grove Street Advisors	Newton	$ 8,300	Fund of Funds
181	Adamas Partners	Boston	$ 8,132	Fund of Funds, Absolute Returns
182	Rockwood Capital	San Francisco	$ 8,132	Real Estate
183	Candlestick Capital	Greenwich	$ 8,048	Equity
184	Weiss Asset Management	Boston	$ 7,986	Multi Strategy, Long/Short
185	Highbridge Capital Management	New York	$ 7,919	Convertibles, Commodities
186	Lombard Odier Darier Hentsch & Cie	Petit-Lancy	$ 7,758	Fund of Funds, Multi Strategy
187	Tilden Park Capital Management	New York	$ 7,690	Multi Strategy, Credit
188	Amber Capital Investment Management	New York	$ 7,661	Managed Futures, Event Driven
189	Harbert Management Corporation	Birmingham	$ 7,659	Emerging Markets, Commodities
190	Trian Fund Management LP	New York	$ 7,634	Event Driven, ESG
191	La Française Global Investment Solutions 	Paris	$ 7,620	Credit, Event Driven
192	Astenbeck Capital Management	Southport	$ 7,584	Commodities
193	Oak Hill Advisors	New York	$ 7,580	Credit, Distressed Assets
194	Atalaya Capital Management LP	New York	$ 7,510	Credit, Special Situations
195	Axonic Capital LLC	New York	$ 7,414	Long/Short, Credit
196	Avenue Capital Group	New York	$ 7,215	Real Estate, Fixed Income
197	Overlook Investments Group	Hong Kong	$ 7,158	
198	Blue Mountain Capital Partners	London	$ 7,100	Managed Futures, Credit
199	The Children's Investment Fund Foundation	London	$ 7,000	Long/Short
200	Emso Asset Management Limited	London	$ 6,885	
201	Gordian Capital	Singapore	$ 6,693	Fund of Funds, Long/Short
202	Capital Fund Management	New York	$ 6,607	Managed Futures
203	Amundi Alternative Investments	Paris	$ 6,580	Fund of Funds, Long/Short
204	Sagard Holdings Manager LP	Toronto	$ 6,536	Multi-Strategy, Credit
205	Antipodes Partners Limited	Sydney	$ 6,364	Global Equities
206	HPS Investment Partners	New York	$ 6,350	Credit
207	York Capital Management	New York	$ 6,335	Event Driven
208	Magnitude Capital	New York	$ 6,303	Fund of Funds, Multi Strategy
209	Kopernik Global Investors	Tampa	$ 6,230	Emerging Markets
210	Bardin Hill Investment Partners	New York	$ 6,216	Multi Strategy, Special Situations
211	Sachem Head Capital Management	New York	$ 6,216	Value
212	Investec Asset Management	London	$ 6,210	Multi Strategy
213	SPX Capital	Rio de Janeiro	$ 6,150	Global Macro, Commodities
214	Deer Park Road Corp	Steamboat Springs	$ 6,114	Distressed Assets, Credit
215	Empyrean Capital Partners	Los Angeles	$ 6,001	Fixed Income, Convertibles
216	Winton Capital Management	London	$ 5,987	Managed Futures, Absolute Returns
217	Gramercy	Greenwich	$ 5,972	Multi Strategy, Emerging Markets
218	HSBC Alternative Investments	London	$ 5,938	Multi Strategy, Global Macro
219	Oxford Asset Management	Oxford	$ 5,889	Absolute Returns, Global Macro
220	Segantii Capital Management	Hong Kong	$ 5,825	Multi Strategy
221	PointState Capital	New York	$ 5,603	Energy, Global Macro
222	VR Advisory Services Ltd.	New York	$ 5,419	Distressed
223	HighVista Strategies	Boston	$ 5,400	Multi Strategy
224	Stone Milliner Asset Management	London	$ 5,380	FX, Global Macro
225	Carlson Alternative Advisors	Dallas	$ 5,357	Private Equity, Multi Strategy
226	Avanda Investment Management	Singapore	$ 5,020	Multi Strategy
227	Fir Tree Partners	New York	$ 4,981	Credit
228	Contrarian Capital Management	Greenwich	$ 4,980	Multi Strategy, Distressed Assets
229	Senvest Capital	New York	$ 4,948	
230	Cantab Capital Partners	Cambridge	$ 4,910	Global Macro, Quantitative
231	Odey Asset Management	London	$ 4,785	Absolute Returns, Long/Short
232	GMT Capital	Atlanta	$ 4,752	Long/Short, Value
233	Indus Capital Partners	New York	$ 4,751	Multi Strategy
234	Evanston Capital Management	Evanston	$ 4,748	Fund of Funds, Multi Strategy
235	Greywolf Capital Management	Purchase	$ 4,727	Special Situations, Structured Products
236	Phoenix Investment Advisers	New York	$ 4,727	Distressed Assets, Fixed Income
237	Wimmer Horizon	London	$ 4,727	Managed Futures, Commodities
238	Seminole Management Company	New York	$ 4,670	Fund of Funds
239	Guggenheim Capital Markets	New York	$ 4,641	Multi Strategy, Fixed Income
240	Kensico Capital Management	Greenwich	$ 4,541	Multi Strategy
241	Aspect Capital	London	$ 4,524	Managed Futures, Long/Short
242	57 Stars	Washington	$ 4,495	Emerging Markets
243	Elementum Advisors	Chicago	$ 4,469	Credit, Distressed Assets
244	Solus Alternative Asset Management	New York	$ 4,250	Distressed Assets
245	Ward Ferry Management	Hong Kong	$ 4,155	Long/Short
246	MKP Capital Europe	London	$ 4,129	Multi Strategy
247	MKP Capital Management	New York	$ 4,129	Multi Strategy, Fixed Income
248	Engineers Gate Manager	New York	$ 4,093	Quantitative
249	Highclere International Investors	London	$ 4,080	Small Cap
250	Rimrock Capital Management	Irvine	$ 4,009	Commodities, Fixed Income
2023 Rank			AUM (Millions)	"""

# Clean and save the data
hedge_funds = clean_hedge_fund_data(raw_data)
save_hedge_funds(hedge_funds)

# Print summary
print(f"Extracted {len(hedge_funds)} hedge fund names")
print("\nFirst 5 funds:")
for fund in hedge_funds[:5]:
    print(f"- {fund}") 