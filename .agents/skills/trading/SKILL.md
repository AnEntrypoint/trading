---
name: trading
description: Systematic and quantitative trading knowledge expressed as semantic anchors in a nonlinear backreferencing mermaid graph, in the style of the llm-coding Semantic-Anchors catalog. Each anchor is a well-defined concept attributable to canonical literature and its authors; naming an anchor activates the whole knowledge cluster. Use for strategy research, factor investing, trend following, mean reversion, options and volatility, portfolio construction, position sizing, backtesting methodology, financial machine learning, market microstructure, execution, behavioral finance, and trading tooling selection.
---

```mermaid
flowchart LR

  subgraph EFF["Market Efficiency Foundations"]
    fama_emh["Efficient Market Hypothesis<br/>Eugene F. Fama (1970) 'Efficient Capital Markets'"]
    samuelson_random["Properly Anticipated Prices Fluctuate Randomly<br/>Paul A. Samuelson (1965)"]
    malkiel_random_walk["Random Walk Hypothesis<br/>Burton G. Malkiel (1973) 'A Random Walk Down Wall Street'"]
    grossman_stiglitz["Grossman-Stiglitz Paradox<br/>Grossman and Stiglitz (1980) 'On the Impossibility of Informationally Efficient Markets'"]
    lo_adaptive_markets["Adaptive Markets Hypothesis<br/>Andrew W. Lo (2004)"]
    mehra_prescott_puzzle["Equity Premium Puzzle<br/>Mehra and Prescott (1985) 'The Equity Premium: A Puzzle'"]
    triumph_optimists["Triumph of the Optimists<br/>Dimson, Marsh and Staunton (2002)"]
    siegel_stocks_long_run["Stocks for the Long Run<br/>Jeremy J. Siegel (1994)"]
  end
  fama_emh --- samuelson_random
  fama_emh --- malkiel_random_walk
  fama_emh --- grossman_stiglitz
  samuelson_random --- malkiel_random_walk
  grossman_stiglitz --- lo_adaptive_markets
  grossman_stiglitz --- pedersen_efficiently_inefficient
  lo_adaptive_markets --- malkiel_random_walk
  mehra_prescott_puzzle --- triumph_optimists
  mehra_prescott_puzzle --- siegel_stocks_long_run
  triumph_optimists --- siegel_stocks_long_run

  subgraph ASP["Asset Pricing Models"]
    markowitz_mpt["Modern Portfolio Theory<br/>Harry Markowitz (1952) 'Portfolio Selection'"]
    tobin_separation["Tobin Separation Theorem<br/>James Tobin (1958) 'Liquidity Preference as Behavior Towards Risk'"]
    capm["Capital Asset Pricing Model<br/>Sharpe (1964), Lintner (1965), Mossin (1966)"]
    ross_apt["Arbitrage Pricing Theory<br/>Stephen A. Ross (1976)"]
    merton_icapm["Intertemporal CAPM<br/>Robert C. Merton (1973)"]
    breeden_ccapm["Consumption CAPM<br/>Douglas T. Breeden (1979)"]
    fama_french_3["Fama-French Three-Factor Model<br/>Fama and French (1992, 1993)"]
    fama_french_5["Fama-French Five-Factor Model<br/>Fama and French (2015)"]
    carhart_4["Carhart Momentum Factor<br/>Mark M. Carhart (1997) 'On Persistence in Mutual Fund Performance'"]
    black_litterman["Black-Litterman Model<br/>Black and Litterman (1992) 'Global Portfolio Optimization'"]
  end
  markowitz_mpt --- tobin_separation
  markowitz_mpt --- capm
  tobin_separation --- capm
  capm --- ross_apt
  capm --- merton_icapm
  merton_icapm --- breeden_ccapm
  capm --- fama_french_3
  fama_french_3 --- fama_french_5
  fama_french_3 --- carhart_4
  fama_french_5 --- carhart_4
  black_litterman --- markowitz_mpt
  black_litterman --- capm

  subgraph FAC["Factor Investing and Cross-Sectional Anomalies"]
    banz_size["Size Premium<br/>Rolf W. Banz (1981)"]
    graham_dodd_value["Value Investing<br/>Graham and Dodd (1934) 'Security Analysis'"]
    novy_marx_profit["Profitability Premium<br/>Robert Novy-Marx (2013) 'The Other Side of Value'"]
    quality_minus_junk["Quality Minus Junk<br/>Asness, Frazzini and Pedersen (2019)"]
    baker_low_vol["Low-Volatility Anomaly<br/>Baker, Bradley and Wurgler (2011) 'Benchmarks as Limits to Arbitrage'"]
    arnott_fundamental_index["Fundamental Indexation<br/>Arnott, Hsu and Moore (2005)"]
    alquist_size_effect["Size Factor: Small Capitalization Stocks Premium<br/>Alquist, Israel and Moskowitz (2018) 'Fact, Fiction, and the Size Effect'"]
    asness_value_ff["Value (Book-to-Market) Factor<br/>Asness, Frazzini, Israel and Moskowitz (2015) 'Fact, Fiction, and Value Investing'"]
    asness_momentum_ff["Momentum Factor Effect in Stocks<br/>Asness, Frazzini, Israel and Moskowitz (2014) 'Fact, Fiction and Momentum Investing'"]
    cooper_asset_growth["Asset Growth Effect<br/>Cooper, Gulen and Schill (2008) 'Asset Growth and the Cross-Section of Stock Returns'"]
    lev_nissim_accrual["Persistence of the Accruals Anomaly<br/>Lev and Nissim (2004)"]
    kozlov_petajisto_eq["Earnings Quality Factor<br/>Kozlov and Petajisto (2012) 'Global Return Premiums on Earnings Quality, Value, and Size'"]
    ang_factor["Factor Investing<br/>Andrew Ang (2014) 'Asset Management'"]
    ilmanen_expected["Expected Returns<br/>Antti Ilmanen (2011)"]
    pedersen_efficiently_inefficient["Efficiently Inefficient<br/>Lasse Heje Pedersen (2015)"]
  end
  fama_french_3 --- banz_size
  fama_french_3 --- graham_dodd_value
  fama_french_5 --- novy_marx_profit
  novy_marx_profit --- quality_minus_junk
  graham_dodd_value --- novy_marx_profit
  capm --- baker_low_vol
  banz_size --- baker_low_vol
  arnott_fundamental_index --- graham_dodd_value
  arnott_fundamental_index --- fama_french_3
  banz_size --- alquist_size_effect
  asness_value_ff --- graham_dodd_value
  asness_momentum_ff --- carhart_4
  cooper_asset_growth --- fama_french_5
  lev_nissim_accrual --- sloan_accrual
  kozlov_petajisto_eq --- sloan_accrual
  kozlov_petajisto_eq --- graham_dodd_value
  ang_factor --- fama_french_3
  ang_factor --- ilmanen_expected
  ilmanen_expected --- carhart_4
  pedersen_efficiently_inefficient --- quality_minus_junk

  subgraph XSMOM["Cross-Sectional Momentum and Earnings Drift"]
    jegadeesh_titman["Cross-Sectional Momentum<br/>Jegadeesh and Titman (1993) 'Returns to Buying Winners and Selling Losers'"]
    chan_jegadeesh_lakonishok["Price and Earnings Momentum<br/>Chan, Jegadeesh and Lakonishok (1996) 'Momentum Strategies'"]
    moskowitz_grinblatt["Industry Momentum<br/>Moskowitz and Grinblatt (1999) 'Do Industries Explain Momentum?'"]
    rouwenhorst_intl["International Momentum<br/>K. Geert Rouwenhorst (1998)"]
    griffin_global_mom["Global Momentum and Business Cycles<br/>Griffin, Ji and Martin (2003)"]
    amp_value_momentum["Value and Momentum Everywhere<br/>Asness, Moskowitz and Pedersen (2013)"]
    novy_marx_intermediate["Intermediate-Horizon Momentum<br/>Robert Novy-Marx (2012) 'Is Momentum Really Momentum?'"]
    george_hwang_52wk["52-Week High Momentum<br/>George and Hwang (2004)"]
    ball_brown["Earnings Announcement Drift Origin<br/>Ball and Brown (1968)"]
    bernard_thomas_pead["Post-Earnings-Announcement Drift<br/>Bernard and Thomas (1989)"]
    daniel_moskowitz_crashes["Momentum Crashes<br/>Daniel and Moskowitz (2016)"]
    barroso_santa_clara["Volatility-Managed Momentum<br/>Barroso and Santa-Clara (2015) 'Momentum Has Its Moments'"]
    blitz_residual_momentum["Residual Momentum Factor<br/>Blitz, Huij and Martens (2011) 'Residual Momentum'"]
    lou_polk_skouras["Overnight Versus Intraday Returns<br/>Lou, Polk and Skouras (2019) 'A Tug of War'"]
    gray_vogel_qm["Quantitative Momentum: A Practitioner's Guide<br/>Gray and Vogel (2016)"]
    sapp_mf_momentum["Momentum in Mutual Fund Returns<br/>Travis Sapp (2010) 'The 52-Week High, Momentum, and Predicting Mutual Fund Returns'"]
    chen_chou_hsieh["Consistent Momentum Strategy<br/>Chen, Chou and Hsieh (2015) 'Persistency of the Momentum Effect'"]
    wei_mom_reversal["Momentum and Reversal Combined with Volatility Effect in Stocks<br/>Jason Zhanshun Wei (2011) 'Do Momentum and Reversals Coexist?'"]
    tibbs_style_rotation["Momentum Factor and Style Rotation Effect<br/>Tibbs, Eakins and DeShurko (2008) 'Using Style Index Momentum to Generate Alpha'"]
    nyberg_poyry["Momentum Factor Combined with Asset Growth Effect<br/>Nyberg and Poyry (2011) 'Firm Expansion and Stock Price Momentum'"]
    hong_jordan_liu["52-Weeks High Effect in Stocks<br/>Hong, Jordan and Liu (2011) 'Industry Information and the 52-Week High Effect'"]
  end
  jegadeesh_titman --- chan_jegadeesh_lakonishok
  jegadeesh_titman --- moskowitz_grinblatt
  jegadeesh_titman --- rouwenhorst_intl
  rouwenhorst_intl --- griffin_global_mom
  griffin_global_mom --- amp_value_momentum
  amp_value_momentum --- jegadeesh_titman
  jegadeesh_titman --- novy_marx_intermediate
  novy_marx_intermediate --- george_hwang_52wk
  chan_jegadeesh_lakonishok --- bernard_thomas_pead
  ball_brown --- bernard_thomas_pead
  ball_brown --- chan_jegadeesh_lakonishok
  jegadeesh_titman --- daniel_moskowitz_crashes
  daniel_moskowitz_crashes --- barroso_santa_clara
  barroso_santa_clara --- blitz_residual_momentum
  blitz_residual_momentum --- jegadeesh_titman
  moskowitz_grinblatt --- blitz_residual_momentum
  lou_polk_skouras --- jegadeesh_titman
  lou_polk_skouras --- george_hwang_52wk
  gray_vogel_qm --- jegadeesh_titman
  gray_vogel_qm --- george_hwang_52wk
  sapp_mf_momentum --- george_hwang_52wk
  sapp_mf_momentum --- carhart_4
  chen_chou_hsieh --- jegadeesh_titman
  wei_mom_reversal --- jegadeesh_titman
  wei_mom_reversal --- jegadeesh_short_reversal
  tibbs_style_rotation --- moskowitz_grinblatt
  nyberg_poyry --- cooper_asset_growth
  nyberg_poyry --- jegadeesh_titman
  hong_jordan_liu --- george_hwang_52wk
  hong_jordan_liu --- moskowitz_grinblatt

  subgraph TREND["Trend Following and Time-Series Momentum"]
    mop_tsm["Time Series Momentum Effect<br/>Moskowitz, Ooi and Pedersen (2012) 'Time Series Momentum'"]
    hurst_century_trend["A Century of Evidence on Trend-Following<br/>Hurst, Ooi and Pedersen (2017)"]
    covel_trend_following["Trend Following<br/>Michael W. Covel (2004)"]
    faith_turtle["Way of the Turtle<br/>Curtis M. Faith (2007)"]
    covel_turtletrader["The Complete TurtleTrader<br/>Michael W. Covel (2007)"]
    antonacci_dual["Dual Momentum<br/>Gary Antonacci (2014)"]
    faber_gtaa["Asset Class Trend-Following (GTAA)<br/>Mebane T. Faber (2007) 'A Quantitative Approach to Tactical Asset Allocation'"]
    faber_ivy["The Ivy Portfolio<br/>Mebane T. Faber (2009)"]
    faber_relative_strength["Momentum Asset Allocation Strategy / Sector Momentum Rotational System<br/>Mebane T. Faber (2010) 'Relative Strength Strategies for Investing'"]
    wilcox_crittenden["Trend-following Effect in Stocks<br/>Wilcox and Crittenden (2005) 'Does Trend Following Work on Stocks?'"]
    maewal_bock["Paired Switching<br/>Maewal and Bock (2011) 'Paired-Switching for Tactical Portfolio Allocation'"]
    faber_global_value["Value Factor: CAPE Effect within Countries<br/>Mebane T. Faber (2012) 'Global Value'"]
  end
  mop_tsm --- hurst_century_trend
  mop_tsm --- jegadeesh_titman
  mop_tsm --- antonacci_dual
  hurst_century_trend --- covel_trend_following
  covel_trend_following --- faith_turtle
  covel_trend_following --- covel_turtletrader
  faith_turtle --- covel_turtletrader
  antonacci_dual --- faber_gtaa
  antonacci_dual --- jegadeesh_titman
  faber_gtaa --- faber_ivy
  faber_gtaa --- mop_tsm
  faber_relative_strength --- faber_gtaa
  faber_relative_strength --- tibbs_style_rotation
  wilcox_crittenden --- covel_trend_following
  wilcox_crittenden --- mop_tsm
  maewal_bock --- faber_gtaa
  faber_global_value --- faber_ivy
  faber_global_value --- graham_dodd_value

  subgraph REV["Reversal, Mean Reversion and Statistical Arbitrage"]
    debondt_thaler_overreaction["Long-Term Overreaction<br/>De Bondt and Thaler (1985) 'Does the Stock Market Overreact?'"]
    jegadeesh_short_reversal["Short-Term Reversal<br/>Narasimhan Jegadeesh (1990) 'Evidence of Predictable Behavior of Security Returns'"]
    lehmann_weekly["Weekly Reversal<br/>Bruce N. Lehmann (1990) 'Fads, Martingales, and Market Efficiency'"]
    lo_mackinlay_contrarian["Contrarian Profits<br/>Lo and MacKinlay (1990) 'When Are Contrarian Profits Due to Stock Market Overreaction?'"]
    gatev_pairs["Pairs Trading with Stocks<br/>Gatev, Goetzmann and Rouwenhorst (2006) 'Pairs Trading: Performance of a Relative-Value Arbitrage Rule'"]
    vidyamurthy_pairs["Pairs Trading: Quantitative Methods<br/>Ganapathy Vidyamurthy (2004)"]
    wang_yu_futures_reversal["Short Term Reversal with Futures<br/>Wang and Yu (2004) 'Trading Activity and Price Reversals in Futures Markets'"]
    degroot_reversal_costs["Short Term Reversal Effect in Stocks<br/>de Groot, Huij and Zhou (2012) 'Another Look at Trading Costs and Short-Term Reversal Profits'"]
    so_wang_news_reversal["Reversal During Earnings-Announcements<br/>So and Wang (2014) 'News-Driven Return Reversals'"]
    zhu_sun_chen_fscore["Combining Fundamental FSCORE and Equity Short-Term Reversals<br/>Zhu, Sun and Chen (2017) 'Noise Trading, Slow Diffusion of Information, and Short-Term Reversals'"]
    schizas_etf_pairs["Pairs Trading with Country ETFs<br/>Schizas, Thomakos and Wang (2011) 'Pairs Trading on International ETFs'"]
  end
  debondt_thaler_overreaction --- lo_mackinlay_contrarian
  debondt_thaler_overreaction --- jegadeesh_short_reversal
  jegadeesh_short_reversal --- lehmann_weekly
  lehmann_weekly --- lo_mackinlay_contrarian
  lo_mackinlay_contrarian --- gatev_pairs
  gatev_pairs --- vidyamurthy_pairs
  gatev_pairs --- jegadeesh_short_reversal
  wang_yu_futures_reversal --- jegadeesh_short_reversal
  degroot_reversal_costs --- jegadeesh_short_reversal
  so_wang_news_reversal --- degroot_reversal_costs
  so_wang_news_reversal --- bernard_thomas_pead
  zhu_sun_chen_fscore --- degroot_reversal_costs
  zhu_sun_chen_fscore --- piotroski_fscore
  schizas_etf_pairs --- gatev_pairs
  vidyamurthy_pairs --- engle_granger_coint

  subgraph CARRY["Carry, Term Structure and Commodity Premia"]
    koijen_carry["Carry Everywhere<br/>Koijen, Moskowitz, Pedersen and Vrugt (2018) 'Carry'"]
    lustig_currency_carry["Dollar Carry Trade<br/>Lustig, Roussanov and Verdelhan (2011) 'Countercyclical Currency Risk Premia'"]
    burnside_carry["Carry Trade Payoffs and Risks<br/>Burnside, Eichenbaum and Rebelo (2011)"]
    db_currency_returns["FX Carry Trade / Currency Momentum Factor / Currency Value Factor PPP Strategy<br/>Deutsche Bank Global Markets Research (2009) 'db Currency Returns'"]
    keynes_backwardation["Normal Backwardation<br/>John Maynard Keynes (1930) 'A Treatise on Money'"]
    working_storage["Theory of Storage<br/>Holbrook Working (1949)"]
    erb_harvey["Commodity Futures Return Decomposition<br/>Erb and Harvey (2006) 'The Strategic and Tactical Value of Commodity Futures'"]
    gorton_rouwenhorst["Facts and Fantasies about Commodity Futures<br/>Gorton and Rouwenhorst (2006)"]
    miffre_rallis["Momentum Effect in Commodities<br/>Miffre and Rallis (2007) 'Momentum Strategies in Commodity Futures Markets'"]
    fuertes_miffre_rallis["Term Structure Effect in Commodities<br/>Fuertes, Miffre and Rallis (2010) 'Tactical Allocation in Commodity Futures Markets'"]
    fernandez_perez_skew["Skewness Effect in Commodities<br/>Fernandez-Perez, Frijns, Fuertes and Miffre (2018) 'The Skewness of Commodity Futures Returns'"]
    durian_padysak["Return Asymmetry Effect in Commodity Futures<br/>Durian and Padysak (2021) 'Return Asymmetry in Commodity Futures'"]
    dunis_wti_brent["Trading WTI/BRENT Spread<br/>Dunis, Laws and Evans (2010) 'Trading and Filtering Futures Spread Portfolios'"]
  end
  koijen_carry --- lustig_currency_carry
  koijen_carry --- burnside_carry
  lustig_currency_carry --- burnside_carry
  lustig_currency_carry --- db_currency_returns
  db_currency_returns --- burnside_carry
  keynes_backwardation --- working_storage
  working_storage --- erb_harvey
  erb_harvey --- gorton_rouwenhorst
  gorton_rouwenhorst --- keynes_backwardation
  miffre_rallis --- mop_tsm
  miffre_rallis --- fuertes_miffre_rallis
  fuertes_miffre_rallis --- working_storage
  fernandez_perez_skew --- gorton_rouwenhorst
  fernandez_perez_skew --- mitton_vorkink_skew
  durian_padysak --- fernandez_perez_skew
  dunis_wti_brent --- vidyamurthy_pairs
  koijen_carry --- amp_value_momentum
  erb_harvey --- koijen_carry

  subgraph VAL["Value, Quality and Defensive Anchors"]
    lsv_contrarian["Contrarian Investment, Extrapolation, and Risk<br/>Lakonishok, Shleifer and Vishny (1994)"]
    piotroski_fscore["Piotroski F-Score<br/>Joseph D. Piotroski (2000)"]
    sloan_accrual["Accrual Anomaly<br/>Richard G. Sloan (1996)"]
    asness_fight_fed["Fight the Fed Model<br/>Clifford S. Asness (2003)"]
    maio_fed_model["The FED Model and Expected Asset Returns<br/>Paulo F. Maio (2008)"]
    blitz_vanvliet_vol["Low Volatility Factor Effect in Stocks<br/>Blitz and van Vliet (2007) 'The Volatility Effect'"]
    frazzini_pedersen_bab["Betting Against Beta Factor in Stocks and International Equities<br/>Frazzini and Pedersen (2014) 'Betting Against Beta'"]
    nagy_esg["ESG Factor Momentum Strategy<br/>Nagy, Kassam and Lee (2016) 'Can ESG Add Alpha?'"]
    esg_stochastic["ESG, Price Momentum and Stochastic Optimization<br/>Quantpedia"]
    chan_rd["R&D Expenditures and Stock Returns<br/>Chan, Lakonishok and Sougiannis (2001) 'The Stock Market Valuation of R&D Expenditures'"]
    chen_zhang_qfactor["ROA Effect within Stocks<br/>Chen and Zhang (2010) 'A Better Three-Factor Model That Explains More Anomalies'"]
    frazzini_lamont_eap["The Earnings Announcement Premium and Trading Volume<br/>Frazzini and Lamont (2007)"]
    amini_singal["Earnings Announcements Combined with Stock Repurchases<br/>Amini and Singal (2015) 'Predictability of Earnings around Corporate Actions'"]
    blitz_vanvliet_gtaa["Value and Momentum Factors across Asset Classes<br/>Blitz and van Vliet (2008) 'Global Tactical Cross-Asset Allocation'"]
  end
  lsv_contrarian --- debondt_thaler_overreaction
  lsv_contrarian --- graham_dodd_value
  piotroski_fscore --- lsv_contrarian
  piotroski_fscore --- sloan_accrual
  sloan_accrual --- bernard_thomas_pead
  asness_fight_fed --- maio_fed_model
  maio_fed_model --- fama_french_3
  blitz_vanvliet_vol --- frazzini_pedersen_bab
  frazzini_pedersen_bab --- baker_low_vol
  frazzini_pedersen_bab --- amp_value_momentum
  nagy_esg --- gray_vogel_qm
  nagy_esg --- esg_stochastic
  chan_rd --- bernard_thomas_pead
  chan_rd --- novy_marx_profit
  chen_zhang_qfactor --- fama_french_5
  chen_zhang_qfactor --- cooper_asset_growth
  frazzini_lamont_eap --- bernard_thomas_pead
  amini_singal --- frazzini_lamont_eap
  blitz_vanvliet_gtaa --- amp_value_momentum
  blitz_vanvliet_gtaa --- faber_gtaa

  subgraph CAL["Calendar and Seasonality Anomalies"]
    rozeff_kinney_january["January Effect<br/>Rozeff and Kinney (1976) 'Capital Market Seasonality'"]
    french_weekend["Weekend Effect<br/>Kenneth R. French (1980)"]
    haugen_lakonishok_january["The Incredible January Effect<br/>Haugen and Lakonishok (1988)"]
    lakonishok_smidt["Calendar Anomalies Ninety-Year Perspective<br/>Lakonishok and Smidt (1988)"]
    ariel_holiday["Holiday Effect<br/>Robert A. Ariel (1990)"]
    bouman_jacobsen_halloween["Halloween Indicator: Sell in May<br/>Bouman and Jacobsen (2002)"]
    hirshleifer_shumway_sun["Good Day Sunshine: Weather and Stock Returns<br/>Hirshleifer and Shumway (2003)"]
    heston_sadka_seas["12 Month Cycle in Cross-Section of Stocks Returns<br/>Heston and Sadka (2008) 'Seasonality in the Cross-Section of Expected Stock Returns'"]
    cooper_jan_barometer["January Barometer<br/>Cooper, McConnell and Ovtchinnikov (2009)"]
    xu_mcconnell_tom["Turn of the Month in Equity Indexes<br/>Xu and McConnell (2006) 'Equity Returns at the Turn of the Month'"]
    ma_pratt_payday["Payday Anomaly<br/>Ma and Pratt (2018)"]
    stivers_sun_opex["Option-Expiration Week Effect<br/>Stivers and Sun (2011)"]
    padysak_vojtko_btc["Overnight Seasonality in Bitcoin<br/>Padysak and Vojtko (2022) 'Seasonality, Trend-following, and Mean Reversion in Bitcoin'"]
    vojtko_overnight_sentiment["Market Sentiment and an Overnight Anomaly<br/>Vojtko and Hanicova (2021)"]
  end
  rozeff_kinney_january --- haugen_lakonishok_january
  rozeff_kinney_january --- lakonishok_smidt
  french_weekend --- lakonishok_smidt
  lakonishok_smidt --- ariel_holiday
  lakonishok_smidt --- xu_mcconnell_tom
  bouman_jacobsen_halloween --- rozeff_kinney_january
  hirshleifer_shumway_sun --- bouman_jacobsen_halloween
  heston_sadka_seas --- rozeff_kinney_january
  heston_sadka_seas --- jegadeesh_titman
  cooper_jan_barometer --- rozeff_kinney_january
  xu_mcconnell_tom --- ma_pratt_payday
  ma_pratt_payday --- ariel_holiday
  stivers_sun_opex --- xu_mcconnell_tom
  stivers_sun_opex --- avellaneda_lipkin_pinning
  padysak_vojtko_btc --- lou_polk_skouras
  vojtko_overnight_sentiment --- padysak_vojtko_btc
  vojtko_overnight_sentiment --- lou_polk_skouras

  subgraph SENT["Sentiment, Flows and Cross-Asset Signals"]
    bernile_lyandres_soccer["Soccer Clubs' Stocks Arbitrage<br/>Bernile and Lyandres (2009) 'Understanding Investor Sentiment: The Case of Soccer'"]
    driesprong_oil["Crude Oil Predicts Equity Returns<br/>Driesprong, Jacobsen and Maat (2008) 'Striking Oil: Another Puzzle?'"]
    padysak_lending["Synthetic Lending Rates Predict Subsequent Market Return<br/>Matus Padysak (2021)"]
    hanicova_lexical["How to Use Lexical Density of Company Filings<br/>Hanicova, Kalus and Vojtko (2021)"]
    padysak_filings["The Positive Similarity of Company Filings and Stock Returns<br/>Matus Padysak (2020)"]
    padysak_smart_factors["Combining Smart Factors Momentum and Market Portfolio<br/>Matus Padysak (2020) 'The Active vs Passive: Smart Factors, Market Portfolio or Both?'"]
    hanicova_rebal_premium["Rebalancing Premium in Cryptocurrencies<br/>Hanicova and Vojtko (2021)"]
    akbas_short_interest["Short Interest Effect: Long-Short Version<br/>Akbas, Boehmer, Erturk and Sorescu (2017) 'Why Do Short Interest Levels Predict Stock Returns?'"]
  end
  bernile_lyandres_soccer --- hirshleifer_shumway_sun
  bernile_lyandres_soccer --- debondt_thaler_overreaction
  driesprong_oil --- granger_causality
  driesprong_oil --- gorton_rouwenhorst
  padysak_lending --- akbas_short_interest
  padysak_lending --- frazzini_pedersen_bab
  hanicova_lexical --- padysak_filings
  hanicova_lexical --- sloan_accrual
  padysak_filings --- bernard_thomas_pead
  padysak_smart_factors --- amp_value_momentum
  padysak_smart_factors --- bogle_index
  hanicova_rebal_premium --- qian_risk_parity
  hanicova_rebal_premium --- padysak_vojtko_btc
  akbas_short_interest --- jegadeesh_short_reversal
  akbas_short_interest --- miller_overpricing

  subgraph OPT["Options and Volatility"]
    subgraph OPTF["Pricing Foundations"]
      black_scholes["Black-Scholes Model<br/>Black and Scholes (1973) 'The Pricing of Options and Corporate Liabilities'"]
      merton_rational["Merton Rational Option Pricing<br/>Robert C. Merton (1973)"]
      stoll_pcp["Put-Call Parity<br/>Hans R. Stoll (1969)"]
      crr_binomial["Binomial Option Pricing Model<br/>Cox, Ross and Rubinstein (1979)"]
      black76["Black-76 Futures Options Model<br/>Fischer Black (1976) 'The Pricing of Commodity Contracts'"]
      harrison_kreps["Martingale Pricing: Fundamental Theorem<br/>Harrison and Kreps (1979)"]
      hull_derivatives["Hull: Options, Futures, and Other Derivatives<br/>John C. Hull (1989)"]
      wilmott_qf["Paul Wilmott on Quantitative Finance<br/>Paul Wilmott (2000)"]
    end
    subgraph VOLM["Volatility Models and the Smile"]
      merton_jump["Merton Jump-Diffusion Model<br/>Robert C. Merton (1976)"]
      heston_sv["Heston Stochastic Volatility Model<br/>Steven L. Heston (1993)"]
      dupire_local_vol["Dupire Local Volatility<br/>Bruno Dupire (1994) 'Pricing with a Smile'"]
      rubinstein_trees["Implied Binomial Trees / Post-1987 Smile<br/>Mark Rubinstein (1994)"]
      hagan_sabr["SABR Model<br/>Hagan, Kumar, Lesniewski and Woodward (2002) 'Managing Smile Risk'"]
      bergomi_smile["Bergomi Smile Dynamics<br/>Lorenzo Bergomi (2004)"]
      gatheral_surface["The Volatility Surface<br/>Jim Gatheral (2006)"]
      rebonato_volcorr["Volatility and Correlation<br/>Riccardo Rebonato (1999)"]
      gatheral_rough["Rough Volatility<br/>Gatheral, Jaisson and Rosenbaum (2018) 'Volatility Is Rough'"]
      engle_arch["ARCH<br/>Robert F. Engle (1982)"]
      bollerslev_garch["GARCH<br/>Tim Bollerslev (1986)"]
    end
    subgraph VARINSTR["Variance Swaps and Volatility Indexes"]
      whaley_vix["Whaley VIX Derivation<br/>Robert E. Whaley (1993) 'Derivatives on Market Volatility'"]
      carr_madan_vs["Variance Swap Replication<br/>Carr and Madan (1998) 'Towards a Theory of Volatility Trading'"]
      britten_neuberger["Model-Free Implied Variance<br/>Britten-Jones and Neuberger (2000)"]
      cboe_vix["CBOE VIX Methodology<br/>CBOE (2003) white paper"]
    end
    subgraph OPTP["Trading and Hedging Practice"]
      option_greeks["The Greeks<br/>John C. Hull (1989) 'Options, Futures, and Other Derivatives'"]
      natenberg["Natenberg: Option Volatility and Pricing<br/>Sheldon Natenberg (1994)"]
      sinclair_vol_trading["Sinclair: Volatility Trading<br/>Euan Sinclair (2008)"]
      sinclair_option_trading["Sinclair: Option Trading<br/>Euan Sinclair (2010)"]
      taleb_dynamic_hedging["Taleb: Dynamic Hedging<br/>Nassim Nicholas Taleb (1997)"]
      avellaneda_lipkin_pinning["Stock Pinning at Expiration<br/>Avellaneda and Lipkin (2003)"]
      bennett_trading_vol["Trading Volatility, Correlation, Term Structure and Skew<br/>Colin Bennett (2014)"]
    end
    subgraph VOLPREM["Option and Volatility Risk Premia"]
      bakshi_kapadia_vrp["Volatility Risk Premium<br/>Bakshi and Kapadia (2003) 'Delta-Hedged Gains'"]
      carr_wu_vrp["Variance Risk Premiums<br/>Carr and Wu (2009)"]
      coval_shumway["Volatility Risk Premium Effect<br/>Coval and Shumway (2001) 'Expected Option Returns'"]
      egloff_leippold_wu["Variance Risk Premium Term Structure<br/>Egloff, Leippold and Wu (2010)"]
      israelov_nielsen_cc["Covered Call Strategies: One Fact and Eight Myths<br/>Israelov and Nielsen (2014)"]
      callan_bxm["BXM Buy-Write Index<br/>Callan Associates (2006)"]
      cboe_put["PUT Put-Write Index<br/>CBOE (2007)"]
      mitton_vorkink_skew["Skewness Preference / Lottery Demand<br/>Mitton and Vorkink (2007)"]
      bali_murray_skew["Risk-Neutral Skewness Premium<br/>Bali and Murray (2013)"]
      driessen_dispersion["Dispersion Trading<br/>Driessen, Maenhout and Vilkov (2009) 'The Price of Correlation Risk'"]
    end
  end
  black_scholes --- merton_rational
  black_scholes --- stoll_pcp
  black_scholes --- crr_binomial
  black_scholes --- black76
  merton_rational --- harrison_kreps
  crr_binomial --- rubinstein_trees
  black76 --- keynes_backwardation
  hull_derivatives --- option_greeks
  wilmott_qf --- hull_derivatives
  black_scholes --- merton_jump
  merton_jump --- heston_sv
  heston_sv --- dupire_local_vol
  dupire_local_vol --- rubinstein_trees
  heston_sv --- hagan_sabr
  hagan_sabr --- bergomi_smile
  bergomi_smile --- gatheral_surface
  gatheral_surface --- dupire_local_vol
  gatheral_surface --- gatheral_rough
  gatheral_rough --- bollerslev_garch
  rebonato_volcorr --- hagan_sabr
  engle_arch --- bollerslev_garch
  bollerslev_garch --- heston_sv
  whaley_vix --- cboe_vix
  carr_madan_vs --- britten_neuberger
  britten_neuberger --- cboe_vix
  carr_madan_vs --- dupire_local_vol
  cboe_vix --- bakshi_kapadia_vrp
  option_greeks --- natenberg
  natenberg --- sinclair_vol_trading
  natenberg --- sinclair_option_trading
  sinclair_vol_trading --- sinclair_option_trading
  taleb_dynamic_hedging --- option_greeks
  taleb_dynamic_hedging --- natenberg
  avellaneda_lipkin_pinning --- option_greeks
  bennett_trading_vol --- rebonato_volcorr
  bennett_trading_vol --- egloff_leippold_wu
  bakshi_kapadia_vrp --- carr_wu_vrp
  carr_wu_vrp --- egloff_leippold_wu
  carr_wu_vrp --- carr_madan_vs
  coval_shumway --- bakshi_kapadia_vrp
  coval_shumway --- bali_murray_skew
  israelov_nielsen_cc --- callan_bxm
  israelov_nielsen_cc --- cboe_put
  callan_bxm --- cboe_put
  cboe_put --- bakshi_kapadia_vrp
  mitton_vorkink_skew --- bali_murray_skew
  bali_murray_skew --- coval_shumway
  driessen_dispersion --- bennett_trading_vol
  driessen_dispersion --- bakshi_kapadia_vrp

  subgraph PCON["Portfolio Construction and Allocation"]
    qian_risk_parity["Risk Parity<br/>Edward Qian (2005) 'Risk Parity Portfolios'"]
    erc_maillard["Equal Risk Contribution<br/>Maillard, Roncalli and Teiletche (2010)"]
    hrp_ldp["Hierarchical Risk Parity<br/>Marcos Lopez de Prado (2016) 'Building Diversified Portfolios that Outperform Out of Sample'"]
    dalio_all_weather["All Weather Strategy<br/>Ray Dalio (2017) 'Principles'"]
    browne_permanent["Permanent Portfolio<br/>Harry Browne (1999) 'Fail-Safe Investing'"]
    swensen_endowment["Endowment Model<br/>David F. Swensen (2000) 'Pioneering Portfolio Management'"]
    grinold_kahn_law["Fundamental Law of Active Management<br/>Grinold and Kahn (1995) 'Active Portfolio Management'"]
    grinold_kahn_risk["Active Risk Decomposition<br/>Grinold and Kahn (2000)"]
    barra_model["Barra Factor Risk Model<br/>Barr Rosenberg (1974) 'Extra-Market Components of Covariance'"]
    carver_systematic["Systematic Trading: A Unique New Method for Designing Trading and Investing Systems<br/>Robert Carver (2015)"]
    carver_leveraged["Leveraged Trading: A Professional Approach<br/>Robert Carver (2019)"]
    chincarini_kim["Quantitative Equity Portfolio Management<br/>Chincarini and Kim (2006)"]
    tomasini_jaekle["Trading Systems: A New Approach to System Development and Portfolio Optimisation / Trading Systems 2nd edition: a new approach to system development and portfolio optimisation<br/>Tomasini and Jaekle (2009, 2019)"]
    guo_lai_quant_trading["Quantitative Trading: Algorithms, Analytics, Data, Models, Optimization<br/>Guo, Lai, Shek and Wong (2017)"]
    grinold_kahn_advances["Advances in Active Portfolio Management: New Developments in Quantitative Investing<br/>Grinold and Kahn (2020)"]
  end
  qian_risk_parity --- erc_maillard
  erc_maillard --- hrp_ldp
  hrp_ldp --- markowitz_mpt
  qian_risk_parity --- dalio_all_weather
  dalio_all_weather --- browne_permanent
  browne_permanent --- bogle_index
  swensen_endowment --- dalio_all_weather
  swensen_endowment --- markowitz_mpt
  grinold_kahn_law --- grinold_kahn_risk
  grinold_kahn_law --- information_ratio
  grinold_kahn_risk --- barra_model
  barra_model --- fama_french_3
  carver_systematic --- carver_leveraged
  carver_systematic --- mop_tsm
  carver_leveraged --- kelly_criterion
  chincarini_kim --- grinold_kahn_law
  chincarini_kim --- barra_model
  tomasini_jaekle --- markowitz_mpt
  guo_lai_quant_trading --- grinold_kahn_law
  grinold_kahn_law --- grinold_kahn_advances

  subgraph PERF["Performance Measurement"]
    sharpe_ratio["Sharpe Ratio<br/>William F. Sharpe (1966) 'Mutual Fund Performance'"]
    sortino_ratio["Sortino Ratio and Downside Deviation<br/>Sortino and van der Meer (1991) 'Downside Risk'"]
    treynor_ratio["Treynor Ratio<br/>Jack L. Treynor (1965)"]
    jensens_alpha["Jensen's Alpha<br/>Michael C. Jensen (1968)"]
    information_ratio["Information Ratio<br/>Thomas H. Goodwin (1998) 'The Information Ratio'"]
    calmar_ratio["Calmar Ratio and Maximum Drawdown<br/>Terry W. Young (1991)"]
    ulcer_index["Ulcer Index<br/>Martin and McCann (1989) 'The Investor's Guide to Fidelity Funds'"]
  end
  sharpe_ratio --- sortino_ratio
  sharpe_ratio --- treynor_ratio
  sharpe_ratio --- information_ratio
  treynor_ratio --- capm
  treynor_ratio --- jensens_alpha
  jensens_alpha --- capm
  jensens_alpha --- grinold_kahn_law
  information_ratio --- grinold_kahn_law
  sortino_ratio --- roy_safety_first
  calmar_ratio --- ulcer_index
  calmar_ratio --- sharpe_ratio
  ulcer_index --- sortino_ratio

  subgraph SIZE["Position Sizing and Money Management"]
    kelly_criterion["Kelly Criterion<br/>John L. Kelly Jr. (1956) 'A New Interpretation of Information Rate'"]
    thorp_beat_dealer["Beat the Dealer<br/>Edward O. Thorp (1962)"]
    kelly_capital_growth["Kelly Capital Growth Criterion<br/>MacLean, Thorp and Ziemba (2011)"]
    fortunes_formula["Fortune's Formula<br/>William Poundstone (2005)"]
    vince_fixed_fractional["Fixed Fractional Sizing<br/>Ralph Vince (1990) 'Portfolio Management Formulas'"]
    vince_optimal_f["Optimal f<br/>Ralph Vince (1992) 'The Mathematics of Money Management'"]
    vince_risk_of_ruin["Risk of Ruin<br/>Ralph Vince (1992) 'The Mathematics of Money Management'"]
    jones_fixed_ratio["Fixed Ratio Sizing<br/>Ryan Jones (1999) 'The Trading Game'"]
    elder_two_percent["Two Percent Rule<br/>Alexander Elder (2002) 'Come Into My Trading Room'"]
    tharp_r_multiples["R-Multiples and Expectancy<br/>Van K. Tharp (1998) 'Trade Your Way to Financial Freedom'"]
    davey_monte_carlo["Monte Carlo Drawdown Simulation<br/>Kevin J. Davey (2014) 'Building Winning Algorithmic Trading Systems'"]
  end
  kelly_criterion --- thorp_beat_dealer
  kelly_criterion --- kelly_capital_growth
  kelly_criterion --- fortunes_formula
  thorp_beat_dealer --- fortunes_formula
  kelly_criterion --- vince_optimal_f
  vince_fixed_fractional --- vince_optimal_f
  vince_optimal_f --- vince_risk_of_ruin
  vince_risk_of_ruin --- davey_monte_carlo
  jones_fixed_ratio --- vince_optimal_f
  elder_two_percent --- vince_fixed_fractional
  elder_two_percent --- vince_risk_of_ruin
  tharp_r_multiples --- vince_fixed_fractional
  tharp_r_multiples --- davey_monte_carlo
  davey_monte_carlo --- walk_forward_pardo

  subgraph DD["Drawdown and Dynamic Risk Control"]
    roy_safety_first["Safety-First Principle<br/>A. D. Roy (1952) 'Safety First and the Holding of Assets'"]
    grossman_zhou_dd["Drawdown-Constrained Optimal Growth<br/>Grossman and Zhou (1993)"]
    chekhlov_cdar["Conditional Drawdown at Risk<br/>Chekhlov, Uryasev and Zabarankin (2005)"]
    kaminski_lo_stoploss["When Do Stop-Loss Rules Stop Losses?<br/>Kaminski and Lo (2014)"]
    moreira_muir_volman["Volatility-Managed Portfolios<br/>Moreira and Muir (2017)"]
    harvey_vol_target["The Impact of Volatility Targeting<br/>Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert (2018)"]
    spitznagel_tail["Tail Risk Hedging<br/>Mark Spitznagel (2013) 'The Dao of Capital'"]
  end
  roy_safety_first --- markowitz_mpt
  grossman_zhou_dd --- kelly_criterion
  grossman_zhou_dd --- calmar_ratio
  chekhlov_cdar --- rockafellar_cvar
  chekhlov_cdar --- grossman_zhou_dd
  kaminski_lo_stoploss --- elder_two_percent
  kaminski_lo_stoploss --- mop_tsm
  moreira_muir_volman --- harvey_vol_target
  moreira_muir_volman --- barroso_santa_clara
  harvey_vol_target --- qian_risk_parity
  harvey_vol_target --- kaminski_lo_stoploss
  spitznagel_tail --- taleb_antifragile
  spitznagel_tail --- bakshi_kapadia_vrp

  subgraph VARTAIL["VaR and Tail Measurement"]
    jorion_var["Value at Risk<br/>Philippe Jorion (1997) 'Value at Risk'"]
    artzner_coherent["Coherent Measures of Risk<br/>Artzner, Delbaen, Eber and Heath (1999)"]
    rockafellar_cvar["CVaR Optimization<br/>Rockafellar and Uryasev (2000)"]
    acerbi_tasche_es["Expected Shortfall Coherence<br/>Acerbi and Tasche (2002)"]
    embrechts_evt["Extreme Value Theory for Finance<br/>Embrechts, Kluppelberg and Mikosch (1997) 'Modelling Extremal Events'"]
    kupiec_stress["Stress Testing in a VaR Framework<br/>Paul H. Kupiec (1998)"]
    basel_1996["Basel Market Risk Amendment<br/>Basel Committee on Banking Supervision (1996)"]
    frtb_2016["FRTB Expected Shortfall Regime<br/>Basel Committee on Banking Supervision (2016) 'Minimum Capital Requirements for Market Risk'"]
  end
  jorion_var --- artzner_coherent
  artzner_coherent --- rockafellar_cvar
  rockafellar_cvar --- acerbi_tasche_es
  acerbi_tasche_es --- frtb_2016
  embrechts_evt --- jorion_var
  embrechts_evt --- mandelbrot_fat_tails
  kupiec_stress --- jorion_var
  kupiec_stress --- basel_1996
  basel_1996 --- frtb_2016
  jorion_var --- engle_arch

  subgraph CRISIS["Fat Tails, Crises and Risk Philosophy"]
    mandelbrot_fat_tails["Stable Paretian Fat Tails<br/>Benoit Mandelbrot (1963) 'The Variation of Certain Speculative Prices'"]
    mandelbrot_misbehavior["The (Mis)behavior of Markets<br/>Mandelbrot and Hudson (2004)"]
    taleb_fooled["Fooled by Randomness<br/>Nassim Nicholas Taleb (2001)"]
    taleb_black_swan["The Black Swan<br/>Nassim Nicholas Taleb (2007)"]
    taleb_antifragile["Antifragile<br/>Nassim Nicholas Taleb (2012)"]
    taleb_skin["Skin in the Game<br/>Nassim Nicholas Taleb (2018)"]
    bali_max_lottery["MAX Lottery Effect<br/>Bali, Cakici and Whitelaw (2011) 'Maxing Out'"]
    crisis_alpha["Crisis Alpha<br/>Hurst, Ooi and Pedersen (2017) 'A Century of Evidence on Trend-Following Investing'"]
    bookstaber_demon["A Demon of Our Own Design<br/>Richard Bookstaber (2007)"]
    when_genius_failed["When Genius Failed: LTCM<br/>Roger Lowenstein (2000)"]
    bernstein_against_gods["Against the Gods: The Remarkable Story of Risk<br/>Peter L. Bernstein (1996)"]
    brown_red_blooded["Red-Blooded Risk<br/>Aaron Brown (2011)"]
    graham_margin_of_safety["Margin of Safety<br/>Benjamin Graham (1949) 'The Intelligent Investor'"]
    miller_overpricing["Divergence of Opinion and Overpricing<br/>Edward M. Miller (1977) 'Risk, Uncertainty, and Divergence of Opinion'"]
  end
  mandelbrot_fat_tails --- mandelbrot_misbehavior
  mandelbrot_fat_tails --- taleb_black_swan
  mandelbrot_misbehavior --- taleb_fooled
  taleb_fooled --- taleb_black_swan
  taleb_black_swan --- taleb_antifragile
  taleb_antifragile --- taleb_skin
  taleb_fooled --- vince_risk_of_ruin
  bali_max_lottery --- mitton_vorkink_skew
  bali_max_lottery --- taleb_black_swan
  crisis_alpha --- hurst_century_trend
  crisis_alpha --- kaminski_lo_stoploss
  bookstaber_demon --- when_genius_failed
  bookstaber_demon --- taleb_black_swan
  when_genius_failed --- kelly_criterion
  when_genius_failed --- graham_margin_of_safety
  bernstein_against_gods --- brown_red_blooded
  bernstein_against_gods --- jorion_var
  brown_red_blooded --- bookstaber_demon
  graham_margin_of_safety --- graham_dodd_value
  graham_margin_of_safety --- roy_safety_first
  miller_overpricing --- taleb_fooled
  miller_overpricing --- debondt_thaler_overreaction

  subgraph BTEST["Backtesting and Strategy Validation"]
    ldp_afml["Advances in Financial Machine Learning<br/>Marcos Lopez de Prado (2018)"]
    walk_forward_pardo["Walk-Forward Analysis<br/>Robert Pardo (2008) 'The Evaluation and Optimization of Trading Strategies'"]
    aronson_ebta["Evidence-Based Technical Analysis<br/>David Aronson (2006)"]
    bailey_pbo["Probability of Backtest Overfitting<br/>Bailey, Borwein, Lopez de Prado and Zhu (2017)"]
    chan_quant_trading["Quantitative Trading<br/>Ernest P. Chan (2008)"]
    chan_algo_trading["Algorithmic Trading: Winning Strategies and Their Rationale<br/>Ernest P. Chan (2013)"]
    chan_machine_trading["Machine Trading: Deploying Computer Algorithms to Conquer the Markets<br/>Ernest P. Chan (2017)"]
    bandy_qta["Quantitative Technical Analysis<br/>Howard B. Bandy (2015)"]
    durenard_pat["Professional Automated Trading<br/>Eugene A. Durenard (2013)"]
    velu_atqs["Algorithmic Trading and Quantitative Strategies<br/>Velu, Hardy and Nehren (2020)"]
    grimes_ta["The Art and Science of Technical Analysis<br/>Adam Grimes (2012)"]
    davey_intro_algo["Introduction To Algo Trading<br/>Kevin J. Davey (2020)"]
  end
  ldp_afml --- bailey_pbo
  ldp_afml --- deflated_sharpe
  ldp_afml --- gu_kelly_xiu
  walk_forward_pardo --- aronson_ebta
  walk_forward_pardo --- bailey_pbo
  aronson_ebta --- whites_reality_check
  bailey_pbo --- deflated_sharpe
  chan_quant_trading --- chan_algo_trading
  chan_algo_trading --- chan_machine_trading
  chan_algo_trading --- engle_granger_coint
  chan_machine_trading --- jansen_ml4t
  bandy_qta --- aronson_ebta
  durenard_pat --- chan_algo_trading
  velu_atqs --- ldp_afml
  grimes_ta --- aronson_ebta
  grimes_ta --- covel_trend_following
  davey_intro_algo --- davey_monte_carlo

  subgraph STATVAL["Multiple Testing and Statistical Validation"]
    deflated_sharpe["Deflated Sharpe Ratio<br/>Bailey and Lopez de Prado (2014)"]
    whites_reality_check["White's Reality Check<br/>Halbert White (2000) 'A Reality Check for Data Snooping'"]
    hansen_spa["Superior Predictive Ability Test<br/>Peter Reinhard Hansen (2005)"]
    model_confidence_set["Model Confidence Set<br/>Hansen, Lunde and Nason (2011)"]
    harvey_liu_zhu["Multiple Testing and the Cross-Section of Expected Returns<br/>Harvey, Liu and Zhu (2016)"]
    harvey_liu_backtest["Backtesting: Haircut Sharpe Ratios<br/>Harvey and Liu (2015)"]
    benjamini_hochberg["False Discovery Rate Control<br/>Benjamini and Hochberg (1995)"]
    lo_mackinlay_snooping["Data-Snooping Biases in Asset Pricing Tests<br/>Lo and MacKinlay (1990)"]
    brown_survivorship["Survivorship Bias in Performance Studies<br/>Brown, Goetzmann, Ibbotson and Ross (1992)"]
    diebold_mariano["Diebold-Mariano Test<br/>Diebold and Mariano (1995) 'Comparing Predictive Accuracy'"]
    stationary_bootstrap["Stationary Bootstrap<br/>Politis and Romano (1994)"]
  end
  deflated_sharpe --- sharpe_ratio
  deflated_sharpe --- harvey_liu_backtest
  whites_reality_check --- hansen_spa
  whites_reality_check --- stationary_bootstrap
  hansen_spa --- model_confidence_set
  model_confidence_set --- diebold_mariano
  harvey_liu_zhu --- harvey_liu_backtest
  harvey_liu_zhu --- benjamini_hochberg
  harvey_liu_zhu --- fama_french_3
  benjamini_hochberg --- whites_reality_check
  lo_mackinlay_snooping --- whites_reality_check
  lo_mackinlay_snooping --- brown_survivorship
  brown_survivorship --- walk_forward_pardo
  stationary_bootstrap --- hansen_spa
  diebold_mariano --- m_competitions

  subgraph ML["Machine Learning for Finance"]
    esl["The Elements of Statistical Learning<br/>Hastie, Tibshirani and Friedman (2001)"]
    breiman_rf["Random Forests<br/>Leo Breiman (2001)"]
    xgboost["XGBoost<br/>Chen and Guestrin (2016)"]
    deep_learning_book["Deep Learning<br/>Goodfellow, Bengio and Courville (2016)"]
    lstm["Long Short-Term Memory<br/>Hochreiter and Schmidhuber (1997)"]
    sutton_barto_rl["Reinforcement Learning: An Introduction<br/>Sutton and Barto (1998)"]
    jansen_ml4t["Machine Learning for Algorithmic Trading<br/>Stefan Jansen (2020)"]
    dixon_ml_finance["Machine Learning in Finance: From Theory to Practice<br/>Dixon, Halperin and Bilokon (2020)"]
    kelly_xiu_survey["Financial Machine Learning<br/>Kelly and Xiu (2023)"]
    gu_kelly_xiu["Empirical Asset Pricing via Machine Learning<br/>Gu, Kelly and Xiu (2020)"]
    ldp_ml_asset["Machine Learning for Asset Managers<br/>Marcos Lopez de Prado (2020)"]
    hilpisch_ai_finance["Artificial Intelligence in Finance<br/>Yves Hilpisch (2020)"]
  end
  esl --- breiman_rf
  breiman_rf --- xgboost
  deep_learning_book --- lstm
  sutton_barto_rl --- dixon_ml_finance
  jansen_ml4t --- ldp_afml
  jansen_ml4t --- gu_kelly_xiu
  dixon_ml_finance --- deep_learning_book
  dixon_ml_finance --- sutton_barto_rl
  kelly_xiu_survey --- gu_kelly_xiu
  kelly_xiu_survey --- esl
  gu_kelly_xiu --- breiman_rf
  gu_kelly_xiu --- harvey_liu_zhu
  ldp_ml_asset --- ldp_afml
  ldp_ml_asset --- hrp_ldp
  hilpisch_ai_finance --- jansen_ml4t

  subgraph TSEC["Time-Series Econometrics"]
    clm_econometrics["The Econometrics of Financial Markets<br/>Campbell, Lo and MacKinlay (1997)"]
    tsay_afts["Analysis of Financial Time Series<br/>Ruey S. Tsay (2001)"]
    hamilton_tsa["Time Series Analysis<br/>James D. Hamilton (1994)"]
    hamilton_regime["Markov Regime Switching<br/>James D. Hamilton (1989)"]
    box_jenkins["Box-Jenkins ARIMA<br/>Box and Jenkins (1970) 'Time Series Analysis: Forecasting and Control'"]
    granger_causality["Granger Causality<br/>Clive W. J. Granger (1969)"]
    engle_granger_coint["Engle-Granger Cointegration<br/>Engle and Granger (1987)"]
    johansen_test["Johansen Cointegration Test<br/>Soren Johansen (1991)"]
    dickey_fuller["Dickey-Fuller Test<br/>Dickey and Fuller (1979)"]
    sims_var["Vector Autoregression<br/>Christopher A. Sims (1980) 'Macroeconomics and Reality'"]
    lo_mackinlay_vr["Variance Ratio Test<br/>Lo and MacKinlay (1988) 'Stock Market Prices Do Not Follow Random Walks'"]
    kalman_filter["Kalman Filter<br/>Rudolf E. Kalman (1960)"]
    m_competitions["M-Competitions<br/>Spyros Makridakis et al. (1982)"]
    gencay_hff["An Introduction to High-Frequency Finance<br/>Gencay, Dacorogna, Muller, Pictet and Olsen (2001)"]
  end
  clm_econometrics --- lo_mackinlay_vr
  clm_econometrics --- tsay_afts
  tsay_afts --- bollerslev_garch
  tsay_afts --- box_jenkins
  hamilton_tsa --- hamilton_regime
  hamilton_tsa --- kalman_filter
  hamilton_tsa --- sims_var
  box_jenkins --- m_competitions
  box_jenkins --- dickey_fuller
  granger_causality --- sims_var
  granger_causality --- engle_granger_coint
  engle_granger_coint --- johansen_test
  engle_granger_coint --- dickey_fuller
  johansen_test --- sims_var
  lo_mackinlay_vr --- fama_emh
  lo_mackinlay_vr --- dickey_fuller
  kalman_filter --- vidyamurthy_pairs
  kalman_filter --- hamilton_regime
  gencay_hff --- tsay_afts
  gencay_hff --- hasbrouck_empirical
  hamilton_regime --- lo_adaptive_markets

  subgraph MICRO["Market Microstructure"]
    subgraph MICT["Microstructure Theory"]
      harris_trading_exchanges["Trading and Exchanges: Market Microstructure for Practitioners<br/>Larry Harris (2003)"]
      ohara_mm_theory["Market Microstructure Theory<br/>Maureen O'Hara (1995)"]
      hasbrouck_empirical["Empirical Market Microstructure<br/>Joel Hasbrouck (2007)"]
      foucault_liquidity["Market Liquidity: Theory, Evidence, and Policy<br/>Foucault, Pagano and Roell (2013)"]
      bouchaud_tqp["Trades, Quotes and Prices<br/>Bouchaud, Bonart, Donier and Gould (2018)"]
      lehalle_practice["Market Microstructure in Practice<br/>Lehalle and Laruelle (2013)"]
      garman_1976["Market Microstructure (Garman)<br/>Mark B. Garman (1976)"]
      demsetz_cost["The Cost of Transacting<br/>Harold Demsetz (1968)"]
      bagehot_1971["The Only Game in Town<br/>Walter Bagehot / Jack L. Treynor (1971)"]
      ho_stoll_dealer["Optimal Dealer Pricing<br/>Ho and Stoll (1981)"]
      roll_spread["Roll's Implicit Spread Estimator<br/>Richard Roll (1984)"]
      glosten_milgrom["Glosten-Milgrom Specialist Model<br/>Glosten and Milgrom (1985)"]
      kyle_lambda["Kyle's Lambda<br/>Albert S. Kyle (1985) 'Continuous Auctions and Insider Trading'"]
      glosten_lob["Electronic Limit Order Book Model<br/>Lawrence R. Glosten (1994)"]
      hasbrouck_info_share["Hasbrouck Information Share<br/>Joel Hasbrouck (1995) 'One Security, Many Markets'"]
      easley_pin["PIN: Probability of Informed Trading<br/>Easley, Kiefer, O'Hara and Paperman (1996)"]
      parlour_queue["Limit Order Queue Dynamics<br/>Christine A. Parlour (1998)"]
      vpin_toxicity["VPIN and Flow Toxicity<br/>Easley, Lopez de Prado and O'Hara (2012)"]
      cont_impact["Order Flow Price Impact<br/>Cont, Kukanov and Stoikov (2014)"]
    end
    subgraph EXEC["Optimal Execution and Market Making"]
      perold_shortfall["Implementation Shortfall<br/>Andre F. Perold (1988)"]
      berkowitz_vwap["VWAP Benchmark<br/>Berkowitz, Logue and Noser (1988) 'The Total Cost of Transactions on the NYSE'"]
      bertsimas_lo_exec["Optimal Control of Execution Costs<br/>Bertsimas and Lo (1998)"]
      almgren_chriss["Almgren-Chriss Optimal Execution<br/>Almgren and Chriss (2001)"]
      kissell_glantz["Optimal Trading Strategies<br/>Kissell and Glantz (2003)"]
      almgren_sqrt["Square-Root Market Impact Law<br/>Almgren, Thum, Hauptmann and Li (2005)"]
      obizhaeva_wang["Supply/Demand Execution Dynamics<br/>Obizhaeva and Wang (2013)"]
      avellaneda_stoikov["Avellaneda-Stoikov Market Making<br/>Avellaneda and Stoikov (2008) 'High-frequency trading in a limit order book'"]
      gueant_liquidity["The Financial Mathematics of Market Liquidity<br/>Olivier Gueant (2016)"]
      cartea_hft["Algorithmic and High-Frequency Trading<br/>Cartea, Jaimungal and Penalva (2015)"]
      kissell_methods["Algorithmic Trading Methods<br/>Robert Kissell (2020)"]
      johnson_dma["Algorithmic Trading and DMA: An Introduction to Direct Access Trading Strategies<br/>Barry Johnson (2010)"]
      narang_black_box["Inside the Black Box: A Simple Guide to Quantitative and High Frequency Trading<br/>Rishi K. Narang (2009)"]
    end
    subgraph MKTDESIGN["Market Design, Latency and HFT"]
      harris_tick["Tick Size Economics<br/>Lawrence E. Harris (1994) 'Minimum Price Variations'"]
      madhavan_mechanisms["Trading Mechanisms Taxonomy<br/>Ananth Madhavan (1992)"]
      madhavan_auctions["Opening Auction Price Discovery<br/>Madhavan and Panchapagesan (2000)"]
      esser_moench_iceberg["Iceberg (Hidden) Orders<br/>Esser and Moench (2007) 'The Navigation of an Iceberg'"]
      ohara_ye_fragmentation["Market Fragmentation<br/>O'Hara and Ye (2011) 'Is Market Fragmentation Harming Market Quality?'"]
      hasbrouck_saar_latency["Low-Latency Trading<br/>Hasbrouck and Saar (2013)"]
      budish_batch["Frequent Batch Auctions<br/>Budish, Cramton and Shim (2015) 'The High-Frequency Trading Arms Race'"]
      reg_nms["Regulation NMS<br/>U.S. Securities and Exchange Commission (2005)"]
      aldridge_hft["High-Frequency Trading<br/>Irene Aldridge (2013)"]
      patterson_dark_pools["Dark Pools: The Rise of A.I. Trading Machines<br/>Scott Patterson (2012)"]
      bodek_hft["The Problem of HFT: Collected Writings<br/>Haim Bodek (2013)"]
      lewis_flash_boys["Flash Boys<br/>Michael Lewis (2014)"]
      ohara_easley_ldp_hft["High-Frequency Trading: New Realities<br/>O'Hara, Easley and Lopez de Prado (2014)"]
    end
  end
  harris_trading_exchanges --- ohara_mm_theory
  harris_trading_exchanges --- reg_nms
  ohara_mm_theory --- kyle_lambda
  ohara_mm_theory --- glosten_milgrom
  hasbrouck_empirical --- roll_spread
  hasbrouck_empirical --- almgren_sqrt
  foucault_liquidity --- glosten_lob
  foucault_liquidity --- kyle_lambda
  bouchaud_tqp --- almgren_sqrt
  bouchaud_tqp --- cont_impact
  lehalle_practice --- almgren_chriss
  lehalle_practice --- reg_nms
  garman_1976 --- demsetz_cost
  garman_1976 --- ho_stoll_dealer
  demsetz_cost --- roll_spread
  bagehot_1971 --- glosten_milgrom
  bagehot_1971 --- kyle_lambda
  ho_stoll_dealer --- avellaneda_stoikov
  glosten_milgrom --- easley_pin
  kyle_lambda --- almgren_sqrt
  glosten_lob --- parlour_queue
  glosten_lob --- foucault_liquidity
  hasbrouck_info_share --- ohara_ye_fragmentation
  hasbrouck_info_share --- kyle_lambda
  easley_pin --- vpin_toxicity
  parlour_queue --- esser_moench_iceberg
  vpin_toxicity --- aldridge_hft
  cont_impact --- bouchaud_tqp
  cont_impact --- glosten_lob
  perold_shortfall --- kissell_glantz
  perold_shortfall --- almgren_chriss
  berkowitz_vwap --- perold_shortfall
  bertsimas_lo_exec --- almgren_chriss
  almgren_chriss --- almgren_sqrt
  almgren_chriss --- perold_shortfall
  kissell_glantz --- berkowitz_vwap
  kissell_glantz --- kissell_methods
  almgren_sqrt --- bouchaud_tqp
  obizhaeva_wang --- almgren_chriss
  obizhaeva_wang --- bertsimas_lo_exec
  avellaneda_stoikov --- gueant_liquidity
  avellaneda_stoikov --- cartea_hft
  gueant_liquidity --- almgren_chriss
  cartea_hft --- aldridge_hft
  cartea_hft --- vpin_toxicity
  kissell_methods --- kissell_glantz
  johnson_dma --- kissell_glantz
  johnson_dma --- harris_trading_exchanges
  narang_black_box --- cartea_hft
  harris_tick --- roll_spread
  harris_tick --- reg_nms
  madhavan_mechanisms --- harris_trading_exchanges
  madhavan_mechanisms --- madhavan_auctions
  madhavan_auctions --- hasbrouck_info_share
  ohara_ye_fragmentation --- reg_nms
  ohara_ye_fragmentation --- patterson_dark_pools
  hasbrouck_saar_latency --- budish_batch
  hasbrouck_saar_latency --- aldridge_hft
  budish_batch --- lewis_flash_boys
  budish_batch --- madhavan_auctions
  reg_nms --- patterson_dark_pools
  aldridge_hft --- hasbrouck_saar_latency
  patterson_dark_pools --- lewis_flash_boys
  bodek_hft --- harris_trading_exchanges
  bodek_hft --- patterson_dark_pools
  lewis_flash_boys --- hasbrouck_saar_latency
  ohara_easley_ldp_hft --- vpin_toxicity
  ohara_easley_ldp_hft --- cartea_hft

  subgraph BEH["Behavioral Finance and Trading Craft"]
    subgraph BEHF["Behavioral Foundations"]
      prospect_theory["Prospect Theory<br/>Kahneman and Tversky (1979)"]
      heuristics_biases["Heuristics and Biases<br/>Tversky and Kahneman (1974) 'Judgment under Uncertainty'"]
      kahneman_tfas["Thinking, Fast and Slow<br/>Daniel Kahneman (2011)"]
      thaler_misbehaving["Misbehaving<br/>Richard H. Thaler (2015)"]
      thaler_nudge["Nudge<br/>Thaler and Sunstein (2008)"]
      barber_odean_hazardous["Trading Is Hazardous to Your Wealth<br/>Barber and Odean (2000)"]
      barber_odean_boys["Boys Will Be Boys: Gender and Overconfidence<br/>Barber and Odean (2001)"]
      shefrin_statman_disposition["Disposition Effect<br/>Shefrin and Statman (1985)"]
      odean_losses["Are Investors Reluctant to Realize Their Losses?<br/>Terrance Odean (1998)"]
      gervais_odean_overconf["Learning to Be Overconfident<br/>Gervais and Odean (2001)"]
    end
    subgraph BEHI["Behavioral Investing"]
      shefrin_beyond["Beyond Greed and Fear<br/>Hersh Shefrin (2000)"]
      montier_behavioral["Behavioural Investing<br/>James Montier (2007)"]
      statman_want["What Investors Really Want<br/>Meir Statman (2010)"]
      housel_psychology["The Psychology of Money<br/>Morgan Housel (2020)"]
    end
    subgraph MANIA["Manias and Market History"]
      shiller_irrational["Irrational Exuberance<br/>Robert J. Shiller (2000)"]
      shiller_narrative["Narrative Economics<br/>Robert J. Shiller (2019)"]
      soros_reflexivity["Reflexivity<br/>George Soros (1987) 'The Alchemy of Finance'"]
      kindleberger_manias["Manias, Panics, and Crashes<br/>Charles P. Kindleberger (1978)"]
      mackay_delusions["Extraordinary Popular Delusions and the Madness of Crowds<br/>Charles Mackay (1841)"]
      galbraith_euphoria["A Short History of Financial Euphoria<br/>John Kenneth Galbraith (1990)"]
      dalio_debt_crises["Big Debt Crises<br/>Ray Dalio (2018)"]
      dalio_world_order["The Changing World Order<br/>Ray Dalio (2021)"]
      mallaby_hedge_funds["More Money Than God<br/>Sebastian Mallaby (2010)"]
    end
    subgraph VCLASSIC["Value Investing Classics"]
      graham_intelligent["The Intelligent Investor: The Definitive Book on Value Investing<br/>Benjamin Graham (1949)"]
      fisher_common_stocks["Common Stocks and Uncommon Profits<br/>Philip A. Fisher (1958)"]
      lynch_one_up["One Up on Wall Street<br/>Peter Lynch (1989)"]
      buffett_essays["The Essays of Warren Buffett<br/>Buffett and Cunningham (1997)"]
      marks_most_important["The Most Important Thing<br/>Howard Marks (2011)"]
      marks_cycle["Mastering the Market Cycle<br/>Howard Marks (2018)"]
      klarman_margin_of_safety["Margin of Safety<br/>Seth A. Klarman (1991)"]
      greenblatt_magic["The Little Book That Beats the Market<br/>Joel Greenblatt (2005)"]
    end
    subgraph CRAFT["Trading Craft and Psychology"]
      schwager_wizards["Market Wizards<br/>Jack D. Schwager (1989)"]
      lefevre_reminiscences["Reminiscences of a Stock Operator<br/>Edwin Lefevre (1923)"]
      elder_trading_living["The New Trading for a Living<br/>Alexander Elder (2014)"]
      douglas_zone["Trading in the Zone<br/>Mark Douglas (2000)"]
      douglas_disciplined["The Disciplined Trader<br/>Mark Douglas (1990)"]
      steenbarger_psych["The Psychology of Trading<br/>Brett N. Steenbarger (2002)"]
      zuckerman_simons["The Man Who Solved the Market<br/>Gregory Zuckerman (2019)"]
      dalio_principles["Principles: Life and Work<br/>Ray Dalio (2017)"]
      nekritin_forex["Naked Forex: High-Probability Techniques for Trading Without Indicators<br/>Nekritin and Peters (2012)"]
      aziz_day_trade["How to Day Trade for a Living<br/>Andrew Aziz (2016)"]
      kratter_beginner["A Beginner's Guide to the Stock Market<br/>Matthew R. Kratter (2019)"]
      snow_quickstart["Investing QuickStart Guide<br/>Ted D. Snow (2018)"]
      noonan_quickstart["Day Trading QuickStart Guide<br/>Troy Noonan (2020)"]
      derman_quant["My Life as a Quant: Reflections on Physics and Finance<br/>Emanuel Derman (2004)"]
      schachter_quants["How I Became a Quant: Insights from 25 of Wall Street's Elite<br/>Barry Schachter (2007)"]
    end
    subgraph CODEBOOK["Coding for Trading"]
      hilpisch_pyfin["Python for Finance: Mastering Data-Driven Finance<br/>Yves Hilpisch (2014)"]
      hilpisch_pyalgo["Python for Algorithmic Trading: From Idea to Cloud Deployment<br/>Yves Hilpisch (2020)"]
      clenow_evolved["Trading Evolved: Anyone Can Build Killer Trading Strategies in Python<br/>Andreas F. Clenow (2019)"]
      conlan_atp["Algorithmic Trading with Python<br/>Chris Conlan (2020)"]
      donadio_lat["Learn Algorithmic Trading: Build and Deploy Algorithmic Trading Systems<br/>Donadio and Ghosh (2019)"]
    end
    subgraph CRYPTOBOOK["Crypto Literature"]
      ammous_bitcoin["The Bitcoin Standard: The Decentralized Alternative to Central Banking<br/>Saifedean Ammous (2018)"]
      mezrich_billionaires["Bitcoin Billionaires: A True Story of Genius, Betrayal, and Redemption<br/>Ben Mezrich (2019)"]
      antonopoulos_mastering["Mastering Bitcoin: Programming the Open Blockchain<br/>Andreas M. Antonopoulos (2017)"]
      edstrom_bitcoin["Why Buy Bitcoin: Investing Today in the Money of Tomorrow<br/>Andy Edstrom (2019)"]
    end
    subgraph PHIL["Investment Philosophy"]
      bernstein_4pillars["The Four Pillars of Investing<br/>William J. Bernstein (2002)"]
      bogle_index["Common Sense Index Investing<br/>John C. Bogle (2007) 'The Little Book of Common Sense Investing'"]
      brown_portnoy["How I Invest My Money: Finance Experts Reveal How They Save, Spend, and Invest<br/>Brown and Portnoy (2020)"]
    end
  end
  prospect_theory --- heuristics_biases
  prospect_theory --- kahneman_tfas
  heuristics_biases --- kahneman_tfas
  kahneman_tfas --- thaler_misbehaving
  thaler_misbehaving --- thaler_nudge
  prospect_theory --- shefrin_statman_disposition
  shefrin_statman_disposition --- odean_losses
  odean_losses --- barber_odean_hazardous
  barber_odean_hazardous --- barber_odean_boys
  barber_odean_boys --- gervais_odean_overconf
  gervais_odean_overconf --- heuristics_biases
  shefrin_beyond --- montier_behavioral
  montier_behavioral --- heuristics_biases
  statman_want --- shefrin_beyond
  statman_want --- housel_psychology
  housel_psychology --- marks_most_important
  shiller_irrational --- shiller_narrative
  shiller_irrational --- kindleberger_manias
  shiller_narrative --- mackay_delusions
  soros_reflexivity --- shiller_irrational
  soros_reflexivity --- marks_cycle
  kindleberger_manias --- mackay_delusions
  kindleberger_manias --- galbraith_euphoria
  galbraith_euphoria --- when_genius_failed
  dalio_debt_crises --- dalio_world_order
  dalio_debt_crises --- kindleberger_manias
  dalio_world_order --- dalio_principles
  mallaby_hedge_funds --- when_genius_failed
  mallaby_hedge_funds --- zuckerman_simons
  graham_intelligent --- graham_margin_of_safety
  graham_intelligent --- buffett_essays
  fisher_common_stocks --- lynch_one_up
  fisher_common_stocks --- buffett_essays
  lynch_one_up --- housel_psychology
  buffett_essays --- marks_most_important
  marks_most_important --- marks_cycle
  marks_most_important --- klarman_margin_of_safety
  marks_cycle --- soros_reflexivity
  klarman_margin_of_safety --- graham_margin_of_safety
  greenblatt_magic --- graham_intelligent
  greenblatt_magic --- quality_minus_junk
  schwager_wizards --- lefevre_reminiscences
  schwager_wizards --- zuckerman_simons
  lefevre_reminiscences --- douglas_zone
  elder_trading_living --- douglas_zone
  elder_trading_living --- elder_two_percent
  douglas_zone --- douglas_disciplined
  douglas_zone --- steenbarger_psych
  douglas_disciplined --- kahneman_tfas
  steenbarger_psych --- kahneman_tfas
  zuckerman_simons --- mallaby_hedge_funds
  dalio_principles --- dalio_all_weather
  dalio_principles --- marks_most_important
  nekritin_forex --- elder_trading_living
  aziz_day_trade --- elder_trading_living
  kratter_beginner --- bogle_index
  snow_quickstart --- kratter_beginner
  noonan_quickstart --- aziz_day_trade
  derman_quant --- taleb_dynamic_hedging
  derman_quant --- wilmott_qf
  schachter_quants --- derman_quant
  hilpisch_pyfin --- hilpisch_pyalgo
  hilpisch_pyfin --- hilpisch_ai_finance
  hilpisch_pyalgo --- chan_algo_trading
  clenow_evolved --- carver_systematic
  clenow_evolved --- mop_tsm
  conlan_atp --- hilpisch_pyalgo
  donadio_lat --- jansen_ml4t
  ammous_bitcoin --- mezrich_billionaires
  ammous_bitcoin --- antonopoulos_mastering
  mezrich_billionaires --- padysak_vojtko_btc
  antonopoulos_mastering --- edstrom_bitcoin
  edstrom_bitcoin --- ammous_bitcoin
  bernstein_4pillars --- markowitz_mpt
  bernstein_4pillars --- bogle_index
  bernstein_4pillars --- housel_psychology
  bogle_index --- fama_emh
  bogle_index --- arnott_fundamental_index
  brown_portnoy --- housel_psychology
  thaler_misbehaving --- debondt_thaler_overreaction
  barber_odean_hazardous --- perold_shortfall
  shefrin_statman_disposition --- kaminski_lo_stoploss
  shiller_irrational --- faber_global_value
  mackay_delusions --- shiller_narrative
  george_hwang_52wk --- heuristics_biases
  bernard_thomas_pead --- heuristics_biases

  subgraph TOOL["Trading Tooling (awesome-systematic-trading inventory)"]
    subgraph TBTE["Event-Driven Backtesting and Live Trading"]
      t_vnpy["vnpy<br/>vnpy team (2015)"]
      t_zipline["zipline<br/>Quantopian (2014)"]
      t_backtrader["backtrader<br/>Daniel Rodriguez (2015)"]
      t_quantaxis["QUANTAXIS<br/>QUANTAXIS community (2017)"]
      t_lean["QuantConnect Lean<br/>Jared Broad / QuantConnect (2012)"]
      t_rqalpha["Rqalpha<br/>Ricequant (2016)"]
      t_finmarketpy["finmarketpy<br/>Saeed Amen / Cuemacro (2016)"]
      t_backtestingpy["backtesting.py<br/>kernc (2019)"]
      t_zvt["zvt<br/>foolcage (2019)"]
      t_wondertrader["WonderTrader<br/>wondertrader team (2020)"]
      t_nautilus["nautilus_trader<br/>Nautech Systems (2018)"]
      t_pandora["PandoraTrader<br/>pegasusTrader (2021)"]
      t_hftbacktest["HFTBacktest<br/>nkaz001 (2020)"]
      t_aat["aat<br/>Tim Paine / AsyncAlgoTrading (2020)"]
      t_sdoosa["sdoosa-algo-trade-python<br/>Sreenivas Doosa (2020)"]
      t_lumibot["lumibot<br/>Lumiwealth (2020)"]
      t_quanttrader["quanttrader<br/>Letian Zhang (2017)"]
      t_gobacktest["gobacktest<br/>gobacktest project (2018)"]
      t_flashfunk["FlashFunk<br/>HFQR (2021)"]
    end
    subgraph TBTV["Vector-Based Backtesting"]
      t_vectorbt["vectorbt<br/>Oleg Polakow (2019)"]
      t_pysystemtrade["pysystemtrade<br/>Robert Carver (2016)"]
      t_bt["bt<br/>Philippe Morissette (2015)"]
    end
    subgraph TCRYPTO["Crypto Trading Frameworks"]
      t_freqtrade["Freqtrade<br/>Freqtrade community (2017)"]
      t_jesse["Jesse<br/>Saleh Mir (2019)"]
      t_octobot["OctoBot<br/>Drakkar-Software (2018)"]
      t_kelp["Kelp<br/>Stellar Development Foundation (2018)"]
      t_openlimits["openlimits<br/>Nash (2020)"]
      t_btrader["bTrader<br/>Gabriel Milan (2021)"]
      t_cryptocrawler["crypto-crawler-rs<br/>crypto-crawler project (2020)"]
      t_hummingbot["Hummingbot<br/>CoinAlpha (2019)"]
      t_cryptotrader["cryptotrader-core<br/>monomadic (2021)"]
    end
    subgraph TBOTS["Trading Bots and Alpha Models"]
      t_blackbird["Blackbird Bitcoin Arbitrage<br/>Julien Hamilton / butor (2016)"]
      t_btcarb["bitcoin-arbitrage<br/>Maxime Biais (2014)"]
      t_thetagang["ThetaGang<br/>brndnmtthws (2021)"]
      t_czsc["czsc<br/>waditu (2020)"]
      t_r2["R2 Bitcoin Arbitrager<br/>bitrinjani (2018)"]
      t_analyzingalpha["analyzingalpha<br/>Leo Smigel (2019)"]
      t_pytrendfollow["PyTrendFollow<br/>chrism2671 (2018)"]
    end
    subgraph TTA["Technical Indicators"]
      t_talib["TA-Lib<br/>Mario Fortier / TA-Lib project (1999)"]
      t_gotart["go-tart<br/>iamjinlei (2020)"]
      t_pandasta["pandas-ta<br/>Kevin Johnson / twopirllc (2019)"]
      t_finta["finta<br/>peerchemist (2017)"]
      t_tarust["ta-rust (ta-rs)<br/>greyblake (2020)"]
    end
    subgraph TMET["Metrics Computation"]
      t_quantstats["quantstats<br/>Ran Aroussi (2019)"]
      t_ffn["ffn<br/>Philippe Morissette (2015)"]
    end
    subgraph TOPT["Portfolio Optimization"]
      t_pyportfolioopt["PyPortfolioOpt<br/>Robert Martin (2018)"]
      t_riskfolio["Riskfolio-Lib<br/>Dany Cajas (2020)"]
      t_empyrial["Empyrial<br/>Santosh Passoubady (2021)"]
      t_deepdow["Deepdow<br/>Jan Krepl (2020)"]
      t_spectre["spectre<br/>Heerozh (2019)"]
    end
    subgraph TPRICE["Derivative Pricing"]
      t_tfquant["tf-quant-finance<br/>Google (2020)"]
      t_financepy["FinancePy<br/>Dominic O'Kane (2020)"]
      t_pyql["PyQL / QuantLib<br/>Luigi Ballabio et al. (2000)"]
    end
    subgraph TRISKT["Risk Analytics"]
      t_pyfolio["pyfolio<br/>Quantopian (2015)"]
    end
    subgraph TBROKER["Broker APIs"]
      t_ccxt["ccxt<br/>Igor Kroitor (2017)"]
      t_ibinsync["ib_insync<br/>Ewald de Wit (2017)"]
      t_coinnect["Coinnect<br/>Hugues (2019)"]
      t_pendax["PENDAX-SDK<br/>CompendiumFi (2022)"]
    end
    subgraph TDATA["Data Sources"]
      t_openbb["OpenBB Terminal<br/>OpenBB (2021)"]
      t_tushare["TuShare<br/>waditu (2014)"]
      t_yfinance["yfinance<br/>Ran Aroussi (2017)"]
      t_akshare["AkShare<br/>AKFamily (2019)"]
      t_datareader["pandas-datareader<br/>PyData team (2015)"]
      t_quandl["Quandl (quandl-python)<br/>Quandl / Nasdaq (2013)"]
      t_findatapy["findatapy<br/>Saeed Amen (2015)"]
      t_investpy["investpy<br/>Alvaro Bartolome (2018)"]
      t_fundamental["Fundamental Analysis Data<br/>Jeroen Bouma (2019)"]
      t_wallstreet["Wallstreet<br/>Mike Dallas (2016)"]
      t_cryptofeed["Cryptofeed<br/>Bryant Moscon (2017)"]
      t_gekko["Gekko-Datasets<br/>xFFFFF (2017)"]
      t_cryptoinscriber["CryptoInscriber<br/>Optixal (2017)"]
      t_cryptolake["Crypto Lake (lake-api)<br/>crypto-lake (2021)"]
    end
    subgraph TDS["Data Science Stack"]
      t_tensorflow["TensorFlow<br/>Google Brain (2015)"]
      t_pytorch["PyTorch<br/>Meta AI (2016)"]
      t_keras["Keras<br/>Francois Chollet (2015)"]
      t_sklearn["scikit-learn<br/>David Cournapeau (2007)"]
      t_pandas["pandas<br/>Wes McKinney (2008)"]
      t_numpy["NumPy<br/>Travis Oliphant (2006)"]
      t_scipy["SciPy<br/>Travis Oliphant et al. (2001)"]
      t_pymc["PyMC<br/>PyMC Developers (2009)"]
      t_cvxpy["CVXPY<br/>Diamond and Boyd (2014)"]
    end
    subgraph TDB["Financial Databases"]
      t_marketstore["Marketstore<br/>Alpaca (2018)"]
      t_tectonicdb["Tectonicdb<br/>0b01 (2017)"]
      t_arcticdb["ArcticDB<br/>Man Group (2015)"]
    end
    subgraph TGRAPH["Graph and Distributed Computation"]
      t_ray["Ray<br/>UC Berkeley RISELab (2017)"]
      t_dask["Dask<br/>Matthew Rocklin (2015)"]
      t_incremental["Incremental<br/>Jane Street (2016)"]
      t_manmdf["Man MDF<br/>Man Group (2016)"]
      t_graphkit["GraphKit<br/>Yahoo (2016)"]
      t_tributary["Tributary<br/>Tim Paine (2018)"]
    end
    subgraph TMLPLAT["ML Trading Platforms"]
      t_qlib["QLib<br/>Microsoft (2020)"]
      t_finrl["FinRL<br/>AI4Finance Foundation (2020)"]
      t_mlfinlab["MlFinLab<br/>Hudson and Thames (2019)"]
      t_tradinggym["TradingGym<br/>Yvictor (2017)"]
      t_dqnbot["Stock Trading Bot Deep Q-Learning<br/>pskrunner14 (2018)"]
    end
    subgraph TTS["Time-Series Analysis"]
      t_prophet["Prophet<br/>Facebook (2017)"]
      t_statsmodels["statsmodels<br/>Seabold and Perktold (2009)"]
      t_tsfresh["tsfresh<br/>Blue Yonder (2016)"]
      t_pmdarima["pmdarima<br/>Taylor G. Smith (2017)"]
    end
    subgraph TVIZ["Visualization"]
      t_dtale["D-Tale<br/>Man Group (2019)"]
      t_mplfinance["mplfinance<br/>Daniel Goldfarb (2019)"]
      t_btplotting["btplotting<br/>happydasch (2020)"]
    end
  end
  t_vnpy --- t_lean
  t_zipline --- t_pyfolio
  t_backtrader --- t_backtestingpy
  t_quantaxis --- t_vnpy
  t_lean --- t_zipline
  t_rqalpha --- t_zipline
  t_finmarketpy --- t_findatapy
  t_backtestingpy --- walk_forward_pardo
  t_zvt --- t_tushare
  t_wondertrader --- t_vnpy
  t_nautilus --- t_hftbacktest
  t_pandora --- t_hftbacktest
  t_hftbacktest --- hasbrouck_empirical
  t_aat --- t_nautilus
  t_sdoosa --- t_backtrader
  t_lumibot --- t_backtestingpy
  t_quanttrader --- t_backtestingpy
  t_gobacktest --- t_backtestingpy
  t_flashfunk --- t_nautilus
  t_vectorbt --- walk_forward_pardo
  t_pysystemtrade --- carver_systematic
  t_bt --- qian_risk_parity
  t_freqtrade --- t_hummingbot
  t_jesse --- t_backtestingpy
  t_octobot --- t_ccxt
  t_kelp --- t_hummingbot
  t_openlimits --- t_ccxt
  t_btrader --- t_ccxt
  t_cryptocrawler --- t_cryptofeed
  t_hummingbot --- avellaneda_stoikov
  t_cryptotrader --- t_ccxt
  t_blackbird --- t_btcarb
  t_btcarb --- t_ccxt
  t_thetagang --- t_ibinsync
  t_czsc --- grimes_ta
  t_r2 --- t_btcarb
  t_analyzingalpha --- jansen_ml4t
  t_pytrendfollow --- mop_tsm
  t_talib --- grimes_ta
  t_talib --- t_gotart
  t_pandasta --- t_talib
  t_finta --- t_pandasta
  t_tarust --- t_finta
  t_quantstats --- sharpe_ratio
  t_ffn --- t_quantstats
  t_pyportfolioopt --- hrp_ldp
  t_riskfolio --- rockafellar_cvar
  t_empyrial --- t_pyportfolioopt
  t_deepdow --- gu_kelly_xiu
  t_spectre --- t_sklearn
  t_tfquant --- heston_sv
  t_financepy --- hull_derivatives
  t_pyql --- hull_derivatives
  t_pyfolio --- t_quantstats
  t_ccxt --- t_cryptofeed
  t_ibinsync --- johnson_dma
  t_coinnect --- t_ccxt
  t_pendax --- t_ccxt
  t_openbb --- t_yfinance
  t_tushare --- t_akshare
  t_yfinance --- t_datareader
  t_akshare --- t_tushare
  t_datareader --- t_quandl
  t_quandl --- t_findatapy
  t_findatapy --- t_finmarketpy
  t_investpy --- t_yfinance
  t_fundamental --- piotroski_fscore
  t_wallstreet --- t_yfinance
  t_cryptofeed --- t_cryptocrawler
  t_gekko --- t_freqtrade
  t_cryptoinscriber --- t_cryptofeed
  t_cryptolake --- t_hftbacktest
  t_tensorflow --- deep_learning_book
  t_pytorch --- deep_learning_book
  t_keras --- t_tensorflow
  t_sklearn --- esl
  t_pandas --- t_numpy
  t_numpy --- t_scipy
  t_scipy --- t_pandas
  t_pymc --- black_litterman
  t_cvxpy --- markowitz_mpt
  t_marketstore --- t_arcticdb
  t_tectonicdb --- t_hftbacktest
  t_arcticdb --- t_pandas
  t_ray --- t_dask
  t_dask --- t_pandas
  t_incremental --- t_manmdf
  t_manmdf --- t_graphkit
  t_graphkit --- t_tributary
  t_tributary --- t_dask
  t_qlib --- gu_kelly_xiu
  t_finrl --- sutton_barto_rl
  t_mlfinlab --- ldp_afml
  t_tradinggym --- sutton_barto_rl
  t_dqnbot --- sutton_barto_rl
  t_prophet --- box_jenkins
  t_statsmodels --- tsay_afts
  t_tsfresh --- t_sklearn
  t_pmdarima --- box_jenkins
  t_dtale --- t_pandas
  t_mplfinance --- t_backtrader
  t_btplotting --- t_backtrader

  subgraph LEARN["Learning Resources (videos, blogs, courses)"]
    subgraph VID["Videos and Interviews"]
      v_krish_naik["Krish Naik ML Tutorials<br/>Krish Naik"]
      v_quantinsti["QuantInsti Webinars<br/>QuantInsti"]
      v_siraj["Siraj Raval Deep Learning for Markets<br/>Siraj Raval"]
      v_quantopian["Quantopian Webinars<br/>Quantopian"]
      v_sentdex["Sentdex ML and Python for Finance<br/>Harrison Kinsley / Sentdex"]
      v_quantnews["QuantNews ML for Algorithmic Trading<br/>QuantNews"]
      v_cwt_mouler["Chat with Traders EP042 and EP142: Bert Mouler<br/>Aaron Fifield / Chat with Traders"]
      v_balch_rl["Applying Deep Reinforcement Learning to Trading<br/>Tucker Balch"]
      v_chan_webinar["Machine Learning for Quantitative Trading Webinar<br/>Ernest P. Chan"]
      v_cwt_starke["Chat with Traders EP147: Tom Starke<br/>Aaron Fifield / Chat with Traders"]
      v_essex_lob["Analyzing the Limit Order Book: A Deep Learning Approach<br/>University of Essex master thesis"]
      v_bandy["Machine Learning Trading System Development Webinar<br/>Howard B. Bandy"]
      v_cwt_slade["Chat with Traders EP131: Morgan Slade<br/>Aaron Fifield / Chat with Traders"]
      v_margenot["Good Uses of Machine Learning in Finance<br/>Max Margenot / Quantopian"]
      v_harada["Deep Learning in Finance Talk<br/>Hitoshi Harada / Alpaca"]
      v_bst_aronson["Better System Trader EP028: David Aronson<br/>Andrew Swanscott / Better System Trader"]
      v_prediction_machines["Prediction Machines: Deep Learning in Finance<br/>Prediction Machines"]
      v_bst_mouler_crypto["Better System Trader EP064: Cryptocurrencies and ML<br/>Andrew Swanscott / Better System Trader"]
      v_bst_himmel["Better System Trader EP023: Michael Himmel<br/>Andrew Swanscott / Better System Trader"]
      v_bst_longmore["Better System Trader EP082: Kris Longmore<br/>Andrew Swanscott / Better System Trader"]
    end
    subgraph BLOG["Blogs"]
      b_aaaquants["AAA Quants Blog<br/>Tom Starke"]
      b_pwb["AI and Systematic Trading Blog<br/>paperswithbacktest"]
      b_blackarbs["Blackarbs Blog<br/>Blackarbs"]
      b_hardikp["Hardikp Blog<br/>Hardik Patel"]
      b_maxdama["Max Dama on Automated Trading<br/>Max Dama"]
      b_medallion["Medallion.Club on Systematic Trading<br/>Medallion.Club"]
      b_proof["Proof Engineering Blog<br/>Proof Engineering"]
      b_quantsportal["Quantsportal Blog<br/>Jacques Joubert"]
      b_quantstart["QuantStart<br/>Michael Halls-Moore"]
      b_robotwealth["RobotWealth Blog<br/>Kris Longmore"]
    end
    subgraph COURSE["Courses"]
      c_cfte["AI in Finance<br/>CFTE"]
      c_pwb["AI and Systematic Trading Course<br/>paperswithbacktest"]
      c_tudorelu["Algorithmic Trading for Cryptocurrencies in Python<br/>tudorelu"]
      c_nyu_tour["Guided Tour of Machine Learning in Finance<br/>NYU / Coursera"]
      c_nyu_fundamentals["Fundamentals of Machine Learning in Finance<br/>NYU / Coursera"]
      c_nyu_rl["Reinforcement Learning in Finance<br/>NYU / Coursera"]
      c_nyu_rl_advanced["Advanced Methods for Reinforcement Learning in Finance<br/>NYU / Coursera"]
      c_hudson_thames["Hudson and Thames Quantitative Research<br/>Hudson and Thames"]
      c_udacity_ai["Artificial Intelligence for Trading<br/>Udacity"]
      c_udacity_ml4t["Machine Learning for Trading<br/>Udacity / Georgia Tech (Tucker Balch)"]
    end
  end
  v_krish_naik --- jansen_ml4t
  v_quantinsti --- chan_algo_trading
  v_siraj --- deep_learning_book
  v_quantopian --- t_zipline
  v_sentdex --- jansen_ml4t
  v_quantnews --- jansen_ml4t
  v_cwt_mouler --- schwager_wizards
  v_balch_rl --- sutton_barto_rl
  v_chan_webinar --- chan_machine_trading
  v_cwt_starke --- b_aaaquants
  v_essex_lob --- bouchaud_tqp
  v_bandy --- bandy_qta
  v_cwt_slade --- gu_kelly_xiu
  v_margenot --- t_zipline
  v_harada --- t_marketstore
  v_bst_aronson --- aronson_ebta
  v_prediction_machines --- deep_learning_book
  v_bst_mouler_crypto --- v_cwt_mouler
  v_bst_himmel --- schwager_wizards
  v_bst_longmore --- b_robotwealth
  b_aaaquants --- ldp_afml
  b_pwb --- mop_tsm
  b_blackarbs --- qian_risk_parity
  b_hardikp --- hilpisch_pyfin
  b_maxdama --- narang_black_box
  b_medallion --- zuckerman_simons
  b_proof --- narang_black_box
  b_quantsportal --- ldp_afml
  b_quantstart --- walk_forward_pardo
  b_robotwealth --- aronson_ebta
  c_cfte --- hilpisch_ai_finance
  c_pwb --- b_pwb
  c_tudorelu --- t_freqtrade
  c_nyu_tour --- c_nyu_fundamentals
  c_nyu_fundamentals --- c_nyu_rl
  c_nyu_rl --- c_nyu_rl_advanced
  c_nyu_rl_advanced --- sutton_barto_rl
  c_hudson_thames --- t_mlfinlab
  c_udacity_ai --- t_qlib
  c_udacity_ml4t --- v_balch_rl

  subgraph EXT["External Semantic-Anchors Catalog Cross-Links"]
    x_mece["MECE Principle<br/>Barbara Minto 'The Minto Pyramid Principle'<br/>(Semantic-Anchors catalog)"]
    x_goodhart["Goodhart's Law<br/>Charles Goodhart (1975)<br/>(Semantic-Anchors catalog)"]
    x_occam["Occam's Razor<br/>William of Ockham<br/>(Semantic-Anchors catalog)"]
    x_first_principles["First Principles Thinking<br/>Aristotle<br/>(Semantic-Anchors catalog)"]
    x_fermi["Fermi Estimation<br/>Enrico Fermi<br/>(Semantic-Anchors catalog)"]
    x_spc["Statistical Process Control / Control Chart<br/>Walter A. Shewhart (1931)<br/>(Semantic-Anchors catalog)"]
    x_devils_advocate["Devil's Advocate<br/>(Semantic-Anchors catalog)"]
    x_cynefin["Cynefin Framework<br/>Dave Snowden (1999)<br/>(Semantic-Anchors catalog)"]
  end
  x_mece --- fama_french_5
  x_goodhart --- deflated_sharpe
  x_goodhart --- sharpe_ratio
  x_occam --- m_competitions
  x_occam --- box_jenkins
  x_first_principles --- markowitz_mpt
  x_fermi --- almgren_sqrt
  x_spc --- walk_forward_pardo
  x_spc --- t_quantstats
  x_devils_advocate --- montier_behavioral
  x_cynefin --- hamilton_regime
  x_cynefin --- lo_adaptive_markets

  sharpe_ratio -.-> kelly_criterion
  markowitz_mpt -.-> harvey_vol_target
  hrp_ldp -.-> bailey_pbo
  carhart_4 -.-> mop_tsm
  baker_low_vol -.-> bakshi_kapadia_vrp
  graham_dodd_value -.-> debondt_thaler_overreaction
  lo_adaptive_markets -.-> hamilton_regime
  ross_apt -.-> gu_kelly_xiu
  black_litterman -.-> t_pymc
  grinold_kahn_law -.-> gu_kelly_xiu
  daniel_moskowitz_crashes -.-> spitznagel_tail
  barroso_santa_clara -.-> harvey_vol_target
  gatev_pairs -.-> engle_granger_coint
  frazzini_pedersen_bab -.-> qian_risk_parity
  koijen_carry -.-> erb_harvey
  heston_sadka_seas -.-> harvey_liu_zhu
  burnside_carry -.-> taleb_black_swan
  bakshi_kapadia_vrp -.-> ang_factor
  coval_shumway -.-> bali_max_lottery
  whaley_vix -.-> hamilton_regime
  mitton_vorkink_skew -.-> housel_psychology
  keynes_backwardation -.-> koijen_carry
  bennett_trading_vol -.-> glosten_milgrom
  avellaneda_lipkin_pinning -.-> stivers_sun_opex
  harrison_kreps -.-> deflated_sharpe
  gu_kelly_xiu -.-> fama_french_5
  sutton_barto_rl -.-> almgren_chriss
  ldp_afml -.-> tharp_r_multiples
  brown_survivorship -.-> jegadeesh_titman
  kelly_criterion -.-> markowitz_mpt
  moreira_muir_volman -.-> baker_low_vol
  spitznagel_tail -.-> coval_shumway
  davey_monte_carlo -.-> bailey_pbo
  when_genius_failed -.-> cont_impact
  almgren_sqrt -.-> vince_optimal_f
  perold_shortfall -.-> walk_forward_pardo
  roll_spread -.-> degroot_reversal_costs
  kyle_lambda -.-> ang_factor
  glosten_milgrom -.-> natenberg
  harris_tick -.-> gencay_hff
  hasbrouck_info_share -.-> lo_mackinlay_contrarian
  vpin_toxicity -.-> harvey_vol_target
  almgren_chriss -.-> markowitz_mpt
  greenblatt_magic -.-> novy_marx_profit
  heuristics_biases -.-> aronson_ebta
  covel_trend_following -.-> walk_forward_pardo
  zuckerman_simons -.-> gu_kelly_xiu
  shiller_narrative -.-> bernile_lyandres_soccer
```
