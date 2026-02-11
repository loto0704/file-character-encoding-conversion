import argparse
import logging
import os
import sys
import shutil
import datetime


def get_arguments() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--input_data', required=True, help='input file')  # 対象ファイル・フォルダ
    arg_parser.add_argument('-be', '--before_encode', required=True, help='before file encode')  # 変換前エンコード
    arg_parser.add_argument('-ae', '--after_encode', required=True, help='after file encode')  # 変換後エンコード
    arg_parser.add_argument('-dg', '--debug_mode', action='store_true', help='debug')  # デバッグモード
    return arg_parser.parse_args()


# ファイルチェック
def check_file(path: str) -> bool | None:
    if os.path.isfile(path):
        logging.info('ファイルチェック：ファイル')
        return True
    elif os.path.isdir(path):
        logging.info('ファイルチェック：フォルダ')
        return False
    else:
        logging.info('ファイルチェック：ファイル&フォルダでもなし')
        return None


# フォルダ作成
def crt_folder(folder_name):
    executable_dir = os.path.dirname(os.path.realpath(__file__))
    crt_folder_path = os.path.join(executable_dir, folder_name).__str__()
    if not os.path.isdir(crt_folder_path):
        os.mkdir(crt_folder_path)
    return crt_folder_path


# フォルダ削除
def delete_folder(folder_name) -> bool:
    try:
        shutil.rmtree(folder_name)
        return True
    except FileNotFoundError:
        print('Folder {} was not deleted'.format(folder_name))
        return False
    except Exception as e:
        logging.error('フォルダ削除:{}'.format(e))
        print('フォルダ削除:{}'.format(e))
        return False


# ロギング
def log_setting(debug_mode: bool):
    log_folder = crt_folder('loggings')
    log_format = '%(asctime)s,%(msecs)d | %(levelname)s | %(name)s - %(message)s'
    log_filepath = os.path.join(log_folder, '{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))).__str__()
    logging.FileHandler(filename=log_filepath, mode='a', encoding='utf-8', delay=False)
    logging.basicConfig(
        filename=log_filepath,
        level=logging.DEBUG if debug_mode else logging.INFO,
        format=log_format,
        encoding='utf-8',
    )
    logging.info('----------ログ開始----------')


# ファイルの文字コードを変換
def concert_encode(file_path, before_encode, after_encode, output_folder):
    try:
        save_path = os.path.join(output_folder, os.path.basename(file_path))
        with open(file=file_path, mode='r', encoding=before_encode) as bf, \
                open(file=save_path, mode='w', encoding=after_encode) as af:
            logging.info('読み込みファイル：{}'.format(file_path))
            logging.info('保存ファイル：{}'.format(save_path))
            try:
                for line in bf:
                    af.write(line)
                logging.info('全行正常終了')
            except Exception as e:
                logging.error('行コピーエラー:{}'.format(e))
                print('行コピーエラー:{}'.format(e))

    except Exception as e:
        logging.error('ファイルの文字コードを変換:{}'.format(e))
        print('ファイルの文字コードを変換:{}'.format(e))


def main():
    args = get_arguments()
    log_setting(args.debug_mode)
    try:
        logging.info('対象ファイル・フォルダ:{}'.format(args.input_data))
        logging.info('変換前エンコード:{}'.format(args.before_encode))
        logging.info('変換後エンコード:{}'.format(args.after_encode))
        logging.info('デバッグモード:{}'.format(args.debug_mode))
        file_or_folder = check_file(args.input_data)
        result_folder = crt_folder(result_folder_name)  # resultフォルダの作成
        output_folder = crt_folder(f'{result_folder}/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}')
        if file_or_folder is None:
            print('ファイル or フォルダを指定ください')
            logging.info('----------ログ終了----------')
            sys.exit(0)
        elif file_or_folder:  # ファイルの場合
            concert_encode(args.input_data, args.before_encode, args.after_encode, output_folder)
        else:  # フォルダの場合
            target_dir = args.input_data
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            for file in files:
                concert_encode(os.path.join(target_dir, file), args.before_encode, args.after_encode, output_folder)

        logging.info('----------ログ終了----------')


    except Exception as e:
        logging.error('main:{}'.format(e))
        print('main:{}'.format(e))
        sys.exit(0)


if __name__ == '__main__':
    result_folder_name = 'results'
    main()
