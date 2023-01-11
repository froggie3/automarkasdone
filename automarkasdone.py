#! python3
import argparse
import pyautogui
import time


def main(iteration, retries):
    print('Press Ctrl-C to quit.')

    try:
        # ウィンドウのフォーカスを切り替える
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('win', 'up')
        pyautogui.hotkey('ctrl', '1')

        for i in range(iteration):
            main_routine(retries)
            i += 1
            
    except KeyboardInterrupt:
        pass


def main_routine(retries):
    # 右側の添付ファイルなどの囲いの範囲を指定
    submit_box_range = (1240, 290, 300, 300)

    # 初期化
    has_attachments = None
    is_button_found = False
    position = None

    # 再読み込みしてロードを待つ
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(5)

    # 一列目のアイテムをクリック
    pyautogui.click(x=920, y=370, button='middle')

    # 開いたタブへフォーカスを切り替える
    pyautogui.hotkey('ctrl', '2')

    # ページのロードを待つ
    time.sleep(3)

    #
    # ボタンを発見して、同時に座標も取得する
    #
    print('「完了としてマーク」のボタンを探しています...')

    for i in range(retries):
        position = pyautogui.locateOnScreen(
            './images/button_marked.png', region=submit_box_range,
            grayscale=True, confidence=0.1)

        # print(i)

        if position is not None:
            print('「完了としてマーク」のボタンを発見しました')
            is_button_found = True
            has_attachments = False
            break

        i += 1

    if is_button_found is False:
        print('次に「提出」のボタンを探しています...')

        for i in range(retries):
            for btn_color in ['./images/button_submit.png',
                              './images/button_submit_green.png']:
                position = pyautogui.locateOnScreen(
                    btn_color, region=submit_box_range,
                    grayscale=True, confidence=0.1)

            # print(i)

            if position is not None:
                print('「提出」のボタンを発見しました')
                has_attachments = True
                break
        i += 1

    if position is None:
        print('ボタンが見当たらなかったため、終了します')
        exit()

    #
    # ボタンを発見して押す ( position は定義済みとする)
    #

    x, y = pyautogui.center(position)
    pyautogui.click(x, y + 10)
    time.sleep(1)

    #
    # モーダルウィンドウにすすむ
    #

    if has_attachments is False:
        print('添付ファイルなしの課題のためそのまま完了としてマークします')

        for i in range(retries):
            for text_color in ['images/text_markasdone_green.png',
                               'images/text_markasdone.png']:
                position = pyautogui.locateOnScreen(
                    text_color, region=(930, 600, 300, 100),
                    confidence=0.1)

            # print(i)

            if position is not None:
                break

            i += 1

        if position is not None:
            x, y = pyautogui.center(position)
            pyautogui.click(x, y)
        else:
            print('確認画面のボタンが見当たらなかったため、終了します')
            exit()
    else:
        print('添付ファイルつきの課題ですがそのまま提出します')

        for i in range(retries):
            for text_color in ['./images/text_submit.png',
                               './images/text_submit_green.png']:
                position = pyautogui.locateOnScreen(
                    text_color, region=(1000, 600, 500, 500),
                    confidence=0.1)

            # print(i)

            if position is not None:
                break

            i += 1

        if position is not None:
            x, y = pyautogui.center(position)
            pyautogui.click(x + 50, y)
            print('提出完了')
        else:
            print('ボタンが見当たらなかったため、強制終了します')
            exit()

    # ロードを待つ
    time.sleep(3)

    # ToDo 画面に戻る
    pyautogui.hotkey('ctrl', 'w')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='automarkasdone.py',
        description='An automation tool to mark a number of assignments on\
                    Google Classroom as making them completed',
        epilog='Make sure your browser to be focused next to your terminal \
                before running this by Alt+Tab.')

    parser.add_argument('iterations', metavar='N', type=int,
                        help='specify how many times to iterate marking as completed')
    parser.add_argument('-r', '--retries', metavar='N', help='specify the number of retry attempts if failed',
                        required=False, type=int, default=5)
    args = parser.parse_args()

    main(iteration=int(args.iterations), retries=int(args.retries))
