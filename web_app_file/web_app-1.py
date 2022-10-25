import streamlit as st 
import numpy as np 
import pandas as pd 
import datetime
import time
import altair as alt


def read_file(file):
    result_file = pd.read_csv(f"web_app_file/df_{file}_30s_30sec.csv") #web_app_file/
    return result_file


list_pairs = ["USDJPY",        
            "AUDJPY",
            "AUDUSD",
            "EURJPY",
            "EURUSD",
            "GBPJPY",
            "NZDJPY",
            "BTCJPY",
            "ETHJPY",
            "BTCUSD",
            "ETHUSD" 
            ]


st.title("スナイプポイント")
st.caption("バイナリーオプション３０秒取引専用ツール")
#変数の定義

start = "2022-03-15"
end = "2022-10-31"

st.sidebar.write(f"""
    ### アルゴリズム可視化アプリ
    ※平日 日本時間 10:00 更新 \n
    
    このツールはアルゴリズム（機関投資家）のタイミングを可視化するアプリです。\n
    
    以下のオプションから分析結果を表示できます。""")
pair_00 = st.sidebar.multiselect("通貨ペアを選択してください。",list_pairs,
                                 ["USDJPY",
                                  "AUDJPY",
                                  "AUDUSD",
                                  "EURJPY",
                                  "EURUSD",
                                  "GBPJPY",
                                  "NZDJPY"
                                  ])


time_sortbox = [] #表示結果の時間をまとめて入れる
result_box = [] #成績が入る
t_hour00 = st.sidebar.select_slider("日本時間(UTC+9)",
                            options=[0,1,2,3,4,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],value=9
                            )
t_list00 = range(0,60,1) # m刻み
t_second_list00 = range(0,60,30) #30秒刻み

win_par00 = st.sidebar.slider("陽線＆陰線の確率[%]",60,99,69,2)

radio_bottun = st.sidebar.radio("対象の期間を選択",
                 ("full year (推奨)","Summer","Winter"))

submit_button = st.sidebar.button("Enter")


if submit_button :
    if not pair_00 :
        
        st.error("error :  通貨ペアを選択してください。")
                 
        
    else :
        latest = st.empty() 
        bar = st.progress(0)
        for num_a in range(100):
            str_box = "分析中"
            if num_a  == 99:
                str_box = "分析完了"
            latest.text(f"{str_box}...{num_a+1}")
            bar.progress(num_a+1)
            time.sleep(0.02)
                    
        
        for i_01 in pair_00:
            if i_01 ==  "EURUSD":
                i_01 = "FX_EURUSD" 
            elif i_01 == "AUDJPY":
                i_01 = "FX_AUDJPY"
            elif i_01 == "AUDUSD":
                i_01 = "FX_AUDUSD"
            elif i_01 == "EURJPY":
                i_01 = "FX_EURJPY"
            elif i_01 == "GBPJPY":
                i_01 = "FX_GBPJPY"
            elif i_01 == "NZDJPY" :
                i_01 = "FX_NZDJPY"
            elif i_01 == "BTCJPY":
                i_01 = "BITFLYER_BTCJPY"
            elif i_01 == "ETHJPY":
                i_01 = "BITFLYER_ETHJPY"
            elif i_01 == "BTCUSD":
                i_01 =  "BITSTAMP_BTCUSD"
            elif i_01 == "ETHUSD":
                i_01 = "COINBASE_ETHUSD"   
                    
    
                
            
            
            pair_01 = read_file(i_01)
            t_hour = t_hour00
            t_list = t_list00
            t_second_list = t_second_list00
            win_par = win_par00
            
            df_01 = pair_01
            df_01["time"] =  pd.to_datetime(df_01["time"]) #datetime型に変換
            df_01 = df_01.set_index("time")#DATE カラムを インデックスにする
            df_01 = df_01.astype(float) #文字列からfloat型に変換
            df_01["week"] = df_01.index.strftime("%a") #曜日を追加
            df_01 = df_01[start:end] #期間の抽出

            time_list = []  #時間を入れる

            y_list = [] #陽線勝率を入れる
            y_median = []#陽線の中央値
            y_mean = []#陽線の平均値
            y_max = []#陽線の最大連続

            i_list = []#陰線勝率
            i_median = []#陰線の中央値
            i_mean = []#陰線の平均値
            i_max = []#陰線の最大連続
            
            



            #for t_hour in t_hour_list:
            for t_min in t_list:
                for t_sec in t_second_list:

                    df_02 = df_01.at_time(f"{t_hour}:{t_min}:{t_sec}") #任意の時間 の検証

                    #for w in week_list: #外せば曜日別ができる
                    df_03 = df_02#[df_02["week"]==w] #外せば曜日別
                    df_open = np.array(df_03["open"])
                    df_close = np.array(df_03["close"])
                    
                    # スプレットを作成
                    num = df_open[0] 
                    num = str(num)
                    num1,num2 = num.split(".") #スプリットで整数と小数点以下を分ける
                    digit = len(num2) #小数点以下が何桁を出す
                    spread = float(f"{num[-1]}e-{digit+1}") # 指数表記とfloatを使って最小の値から１桁小さいスプレットを出す。
                    
                    
                    down=df_open-spread > df_close #オープンのほうが数値が大きい＝陰線
                    down_minus = down[:-1] 
                    
                    up = df_open+spread < df_close #オープンのほうが数値が小さい＝陽線
                    up_minus = up[:-1]
                    
                    insen = np.count_nonzero(down)/len(df_open) #陰線確率  Trueの数を数えている
                    insen_minus = np.count_nonzero(down_minus)/len(down_minus) #前回の陰線勝率
                    yousen =  np.count_nonzero(up)/len(df_open) #陽線確率 
                    yousen_minus =  np.count_nonzero(up_minus)/len(up_minus) #前回の勝率
                    
                    #print(f"陰線 {i},{insen*100:.04g}%") #週別のときに使う
                    #print(f"陽線 {i},{yousen*100:.04g}%")#週別の時に使う
                    #print(f"{t_hour}時{t_min}分エントリー")#週別の時に使う
                    #print("----------------")
                    time_list.append(f"{t_hour}:{t_min}:{t_sec}")

                    
                    result = 0
                    box_y = []
                    for c,o in zip(df_close,df_open): 
                        if c - o > 0:
                            r = c-o #終値から始値を引いた数字をｒに入れる
                            box_y.append(r) #boxにリストとして追加していく
                            result += r #resultに追加していく
                    y_median.append(round(np.median(box_y),4))
                    y_mean.append(round(np.mean(box_y),4))


                    result = 0
                    box_i = []

                    for c,o in zip(df_close,df_open): 
                            if o - c > 0:
                                r = o - c #始値から終値を引いた数字をｒに入れる
                                box_i.append(r) #boxにリストとして追加していく
                                result += r #resultに追加していく

                    i_median.append(round(np.median(box_i),4))
                    i_mean.append(round(np.mean(box_i),4))



                    data_y = pd.DataFrame({"group" :df_open + spread < df_close}) #陽線はTrue、陰線はFalse
                    
                    box1 = 0
                    box_max_y = 1
                    for i in data_y["group"]:
                        if i == True:
                            box1 += 1
                        elif i == False:
                            box1 = 0
                        if box1 > box_max_y:
                            box_max_y = box1

                    y_max.append(box_max_y)

                    data_i = pd.DataFrame({"group" :df_open > df_close}) #陽線はFalse、陰線はTrue

                    box1 = 0
                    box_max_i = 1
                    for i in data_i["group"]:
                        if i == True: 
                            box1 += 1
                        elif i == False:
                            box1 = 0
                        if box1 > box_max_i:
                            box_max_i = box1

                    i_max.append(box_max_i)

                    # 大路チャート

                    dairo_list= [] #勝ち負けをすべて格納する


                    dairo_list_1 = [[]*i for i in range(20)]  #内包表記で大量のリストを作成
                    list_num = 0

                    for i , y in zip(data_i["group"],data_y["group"]):
                        if i == False:  #i がFalse ということは 陽線
                            dairo_list += "1"


                        if y == False: # Falseで 負け（陰線 + 十字足） ｙが Falseということは 陰線 or 十字足
                            dairo_list += "0"
                            
                    #大路チャートを作成する関数  連続した動きだけを抽出して それを リストに追加していく
                    
                    def dairo_chart(list_num): 
                        y = None
                        for i,num in zip(dairo_list,range(100)):
                            if y == None: #初めの１回目がエラーになるため１回目のためだけに書いておく
                                y = i

                            if y != i :
                                del dairo_list[0:num]
                                dairo_back = dairo_list
                                break

                            if i == "1":
                                dairo_list_1[list_num] += "〇"

                            elif i == "0":
                                dairo_list_1[list_num] += "×"   



                        return dairo_list

                    #作った関数で 任意の回数 行い 連続した動きを取り出す
                    for i in range(20):
                        dairo_chart(i)

                    #同じリストが重複したら それ以降は 消す
                    for i, x , z in zip(dairo_list_1,dairo_list_1[1:],range(100)):
                        if i == x:
                            dairo_list_1[z+1:] = []


                    #データフレームにして 転置する
                    df_dairo = pd.DataFrame(dairo_list_1).T
                    df_dairo = df_dairo.fillna("")
                    
                    if insen_minus*100 >= win_par:
                        " *** " 
                        #直近の勝敗を記録
                        y_result = list(data_y["group"])[-1]
                        i_result = list(data_i["group"])[-1]
                        
                        if i_result == True:
                            result_box.append("1")
                        else:
                            result_box.append("0")
                            
                        
                        time_sortbox.append(f"{i_01}【Short】-- {t_hour}:{t_min}:{t_sec}")
                        st.write(f"{i_01}")
                        st.write(f"UTG+9 :{t_hour}時{t_min}分{t_sec}秒:【 Short 】")
                        st.write(f"エントリー前の勝率{insen_minus*100:.04g}%")
                        st.write(f"エントリー後の勝率{insen*100:.04g}%")
                        st.write("陰線中央値",np.median(box_i).round(4),"陰線平均値",np.mean(box_i).round(4),"Volume中央値",np.median(df_03["Volume"])) #中央値と平均値
                        st.write(f"最大連続陰線{box_max_i}")
                        st.table(df_dairo)
                        
                    
                    #陰線勝率 チャート
                        box_chart01_i = []
                        box_result_i = []
                        for i in data_i["group"]:
                            box_chart01_i.append(i)
                            box_01 = np.count_nonzero(box_chart01_i)
                            result_cha = box_01 / len(box_chart01_i)
                            box_result_i.append(round(result_cha*100,2))
                            
                        result_chart = pd.DataFrame({
                                        "陰線":box_result_i
                                        })         
                        result_chart = result_chart.tail(15)
                        result_chart["X_label"] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                                                                        
                         # altair 
                        chart=alt.Chart(result_chart).mark_line(opacity=0.8,clip=True,point=alt.OverlayMarkDef(color="red")).encode( #折れ線は mark_line  引数はなくてもいい opacityは不透明度 clipは 枠以外のチャートを非表示
                                alt.X("X_label",title = "時系列",scale=alt.Scale(domain=[0,16])),                            #x=X_labelでもOK この場合は 細かい設定titleなども変えたかったから この形
                                alt.Y("陰線:Q",title = "勝率(%)",scale=alt.Scale(domain=[50,100])),
                                )
                        text =chart.mark_text(color = "gray",
                                align = "center", #left,center,right
                                baseline = "top",#top,middle,bottom
                                dx = 18).encode(
                                text="陰線"
                                
                                )
                        chart_text=(chart + text).properties(height=600,width=720)
                        chart_text
                        
                    if yousen_minus*100 >= win_par:
                        " *** "
                        #直近の勝敗を記録                        
                        y_result = list(data_y["group"])[-1]
                        i_result = list(data_i["group"])[-1]
                        
                        if y_result == True:
                            result_box.append("1")
                        else:
                            result_box.append("0")
                        
                        time_sortbox.append(f"{i_01}【Long】-- {t_hour}:{t_min}:{t_sec}")
                        st.write(f"{i_01}")
                        st.write(f"UTG+9 :{t_hour}時{t_min}分{t_sec}秒:【 Long 】")
                        st.write(f"エントリー前の勝率{yousen_minus*100:.04g}%")
                        st.write(f"エントリー後の勝率{yousen*100:.04g}%")
                        st.write("陽線中央値",np.median(box_y).round(4),"陽線平均値",np.mean(box_y).round(4),"Volume中央値",np.median(df_03["Volume"])) #中央値と平均値
                        st.write(f"最大連続陽線{box_max_y}")
                        st.table(df_dairo)
                        #陽線勝率 チャート
                        box_chart01_y = []
                        box_result_y = []
                        for i in data_y["group"]:
                            box_chart01_y.append(i)
                            box_01 = np.count_nonzero(box_chart01_y)
                            result_cha = box_01 / len(box_chart01_y)
                            box_result_y.append(round(result_cha*100,2))
                        
                        result_chart = pd.DataFrame({
                                        "陽線":box_result_y,
                                        
                                        })         
                        result_chart = result_chart.tail(15)
                        result_chart["X_label"] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
                        
                        
                        
                         # altair 
                        chart=alt.Chart(result_chart).mark_line(opacity=0.8,clip=True,point=alt.OverlayMarkDef(color="red")).encode( #折れ線は mark_line  引数はなくてもいい opacityは不透明度 clipは 枠以外のチャートを非表示
                                alt.X("X_label",title = "時系列",scale=alt.Scale(domain=[0,16])),                            #x=X_labelでもOK この場合は 細かい設定titleなども変えたかったから この形
                                alt.Y("陽線:Q",title = "勝率(%)",scale=alt.Scale(domain=[50,100])),
                                )
                        text =chart.mark_text(
                                color = "gray",
                                align = "center", #left,center,right
                                baseline = "top",#top,middle,bottom
                                dx = 18).encode(
                                text="陽線"
                                )
                        chart_text=(chart + text).properties(height=600,width=720)
                        chart_text
        """
        ### 【Result】
        """
        for i in time_sortbox:
            st.write(i)
        
        result_win = result_box.count("1")
        result_lose = result_box.count("0")
        st.write(f"{result_win}勝{result_lose}敗")

                                

            
            

                    
