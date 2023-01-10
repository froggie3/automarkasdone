#! python3
import pyautogui
import time

print('Press Ctrl-C to quit.')

# 右側の添付ファイルなどの囲いの範囲を指定
submit_box_range = (1240, 290, 300, 300)

# 初期化
tries = 10
has_attachments = None
is_button_found = False
p = None

try:
    # ウィンドウのフォーカスを切り替える
    pyautogui.hotkey("alt", "tab")
    pyautogui.hotkey("ctrl", "1")

    for i in range(53):
        # 再読み込みしてロードを待つ
        pyautogui.hotkey("ctrl", "r")
        time.sleep(5)

        # 一列目のアイテムをクリック
        pyautogui.click(x=920, y=370, button='middle')

        # 開いたタブへフォーカスを切り替える
        pyautogui.hotkey("ctrl", "2")

        # ページのロードを待つ
        time.sleep(3)

        """
        ボタンを発見して、同時に座標も取得する
        """
        print("「完了としてマーク」のボタンを探しています...")

        for i in range(tries):
            p = pyautogui.locateOnScreen(
                "./images/button_marked.png", region=submit_box_range, grayscale=True, confidence=0.1)

            # print(i)

            if p is not None:
                print("「完了としてマーク」のボタンを発見しました")
                is_button_found = True
                has_attachments = False
                break

        if is_button_found is False:
            print("次に「提出」のボタンを探しています...")

            for i in range(tries):
                for btn_color in ["./images/button_submit.png", "./images/button_submit_green.png"]:
                    p = pyautogui.locateOnScreen(
                        btn_color, region=submit_box_range, grayscale=True, confidence=0.1)

                # print(i)

                if p is not None:
                    print("「提出」のボタンを発見しました")
                    has_attachments = True
                    break

        if p is None:
            print("ボタンが見当たらなかったため、終了します")
            exit()

        """
        ボタンを発見して押す ( p は定義済みとする)
        """

        x, y = pyautogui.center(p)
        pyautogui.click(x, y + 10)
        time.sleep(1)

        """
        モーダルウィンドウにすすむ
        """

        if has_attachments is False:
            print("添付ファイルなしの課題のためそのまま完了としてマークします")

            for i in range(tries):
                for text_color in ["images/text_markasdone_green.png", "images/text_markasdone.png"]:
                    p = pyautogui.locateOnScreen(
                        text_color, region=(930, 600, 300, 100), confidence=0.1)

                # print(i)

                if p is not None:
                    break

            if p is not None:
                x, y = pyautogui.center(p)
                pyautogui.click(x, y)
            else:
                print("確認画面のボタンが見当たらなかったため、終了します")
                exit()
        else:
            print("添付ファイルつきの課題ですがそのまま提出します")

            for i in range(tries):
                for text_color in ["./images/text_submit.png", "./images/text_submit_green.png"]:
                    p = pyautogui.locateOnScreen(
                        text_color, region=(1000, 600, 500, 500), confidence=0.1)

                # print(i)

                if p is not None:
                    break

            if p is not None:
                x, y = pyautogui.center(p)
                pyautogui.click(x + 50, y)
                print("提出完了")
            else:
                print("ボタンが見当たらなかったため、強制終了します")
                exit()

        # ロードを待つ
        time.sleep(3)

        # ToDo 画面に戻る
        #pyautogui.hotkey("ctrl", "shift", "tab")
        pyautogui.hotkey("ctrl", "w")

        i += 1
except KeyboardInterrupt:
    print('\n')
