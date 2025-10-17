import logging
import requests
import time
import os
import re
import logging
import threading
import guessit
from dotenv import load_dotenv
from p123client.tool import get_downurl
from p123client import P123Client
# 加载.env文件中的环境变量
load_dotenv(dotenv_path="db/user.env",override=True)
load_dotenv(dotenv_path="sys.env",override=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置日志级别为INFO，确保info级别的日志能被输出
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 创建缓存字典，用于存储文件名对应的fileid、download_url，以及缓存时间
# 格式: {filename: (fileid, download_url, timestamp)}
url_cache1 = {}
url_cache2 = {}
url_cache3 = {}
url_cache4 = {}
url_cache5 = {}
if os.getenv('123_xiaohao_passport1', "") and os.getenv('123_xiaohao_password1', ""):
    try:
        client_xiaohao1 = P123Client(os.getenv('123_xiaohao_passport1', ""),os.getenv('123_xiaohao_password1', ""))
    except Exception as e:
        logger.error(f"创建123客户端1失败: {e}")
        client_xiaohao1 = None
if os.getenv('123_xiaohao_passport2', "") and os.getenv('123_xiaohao_password2', ""):
    try:
        client_xiaohao2 = P123Client(os.getenv('123_xiaohao_passport2', ""),os.getenv('123_xiaohao_password2', ""))
    except Exception as e:
        logger.error(f"创建123客户端2失败: {e}")
        client_xiaohao2 = None
if os.getenv('123_xiaohao_passport3', "") and os.getenv('123_xiaohao_password3', ""):
    try:
        client_xiaohao3 = P123Client(os.getenv('123_xiaohao_passport3', ""),os.getenv('123_xiaohao_password3', ""))
    except Exception as e:
        logger.error(f"创建123客户端3失败: {e}")
        client_xiaohao3 = None
if os.getenv('123_xiaohao_passport4', "") and os.getenv('123_xiaohao_password4', ""):
    try:
        client_xiaohao4 = P123Client(os.getenv('123_xiaohao_passport4', ""),os.getenv('123_xiaohao_password4', ""))
    except Exception as e:
        logger.error(f"创建123客户端4失败: {e}")
        client_xiaohao4 = None
if os.getenv('123_xiaohao_passport5', "") and os.getenv('123_xiaohao_password5', ""):
    try:
        client_xiaohao5 = P123Client(os.getenv('123_xiaohao_passport5', ""),os.getenv('123_xiaohao_password5', ""))
    except Exception as e:
        logger.error(f"创建123客户端5失败: {e}")
        client_xiaohao5 = None
CACHE_EXPIRATION = 720 * 60  # 缓存有效期，30分钟（秒）
def get_int_env(env_name, default_value=0):
    try:
        value = os.getenv(env_name, str(default_value))
        return int(value) if value else default_value
    except (ValueError, TypeError):
        logger.warning(f"环境变量 {env_name} 值不是有效的整数，使用默认值 {default_value}")
        return default_value
# 创建父目录ID缓存字典，用于存储父目录ID的缓存时间
# 格式: {parent_file_id: timestamp}
parent_dir_cache = {}
PARENT_DIR_CACHE_EXPIRATION = 12 * 3600  # 父目录ID缓存有效期，12小时（秒）

# 创建弹幕下载缓存字典，用于存储文件路径对应的缓存时间
# 格式: {file_path: timestamp}
danmu_cache = {}
DANMU_CACHE_EXPIRATION = 12 * 3600  # 弹幕下载缓存有效期，12小时（秒）

# 线程锁，用于确保precache_parent_directory_files函数同一时间只能运行一个实例
precache_lock = threading.Lock()
from danmu import download_danmaku
def get_token_from_config() -> str:
    """从db目录下的config.txt文件中读取token"""
    config_path = os.path.join('db', 'config.txt')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            token = f.read().strip()
            logger.info("成功从配置文件读取token")
            return token
    except Exception as e:
        logger.error(f"读取配置文件失败: {str(e)}")
        raise Exception(f"无法从配置文件读取token: {str(e)}")

def get_download_url_by_path_xiaohao(file_path: str, i) -> str:
    """
    从文件路径中提取文件名并搜索文件，返回与文件名完全匹配且文件大小最大的文件的下载直链
    优先使用缓存中的链接（有效期30分钟）
    参数:
        file_path: 完整的文件路径，例如："/CloudNAS/CloudDrive/123云盘/Video/通用格式影视库/电视节目/国产剧集/2025/侠医 (2025) {tmdb-298444}/Season 1/侠医.2025.S01E01.第1集.1080p.MyTVSuper.WEB-DL.H.265.mkv"
    返回:
        字符串 (下载直链)，如果没有找到匹配项则返回 None
    """
    if i == 1:
        client = client_xiaohao1
        url_cache = url_cache1
    elif i == 2:
        client = client_xiaohao2
        url_cache = url_cache2
    elif i == 3:
        client = client_xiaohao3
        url_cache = url_cache3
    elif i == 4:
        client = client_xiaohao4
        url_cache = url_cache4
    elif i == 5:
        client = client_xiaohao5
        url_cache = url_cache5
    else:
        logger.error(f"无效的客户端索引: {i}")
        return None
    if os.getenv('DANMAKU_API_URL', "") and os.getenv('DANMAKU_API_KEY', ""):
        # 检查弹幕下载缓存
        current_time = time.time()
        if file_path in danmu_cache:
            cache_time = danmu_cache[file_path]
            if current_time - cache_time < DANMU_CACHE_EXPIRATION:
                remaining_time = (DANMU_CACHE_EXPIRATION - (current_time - cache_time)) / 3600
                logger.info(f"弹幕下载已缓存，剩余有效期: {remaining_time:.1f}小时，跳过下载操作")
            else:
                # 缓存已过期，执行弹幕下载
                logger.info("弹幕下载缓存已过期，重新执行下载操作")
                download_danmaku(file_path)
                # 更新缓存时间
                danmu_cache[file_path] = current_time
        else:
            # 缓存不存在，执行弹幕下载
            logger.info("弹幕下载缓存不存在，执行下载操作")
            download_danmaku(file_path)
            # 设置缓存时间
            danmu_cache[file_path] = current_time
        
    # 从文件路径中提取文件名（包含扩展名）作为缓存键
    file_name_with_ext = os.path.basename(file_path)
    
    # 检查缓存中是否有有效链接
    current_time = time.time()
    file_id = None
    if file_name_with_ext in url_cache:
        file_id, cached_url, cache_time = url_cache[file_name_with_ext]
        if (current_time - cache_time < CACHE_EXPIRATION) and cached_url:
            logger.info(f"使用缓存的下载链接，剩余有效期: {(CACHE_EXPIRATION - (current_time - cache_time))/60:.1f}分钟")
            return cached_url
        else:
            del url_cache[file_name_with_ext]  # 删除过期缓存
    
    # 记录从文件路径提取的搜索关键词
    logger.info(f"从文件路径提取的搜索关键词: {file_name_with_ext}")
    
    # 去除文件名中的中文符号
    #cleaned_file_name = remove_chinese_symbols(file_name_with_ext)
    #logger.info(f"去除中文符号后的搜索关键词: {cleaned_file_name}")
    cleaned_file_name = file_name_with_ext
    # 2. 使用处理后的文件名调用搜索API
    all_items = []
    try:
        # 从配置文件获取token
        token = get_token_from_config()
        search_url = f"https://www.123pan.com/b/api/file/list/new?driveId=0&limit=100&next=0&orderBy=update_time&orderDirection=desc&parentFileId=0&trashed=false&SearchData={cleaned_file_name}&Page=1&OnlyLookAbnormalFile=0&event=homeListFile&operateType=2&inDirectSpace=false"
        headers = {
            'Authorization': f'Bearer {token}',
            'Platform': 'web'
        }           
        response = requests.get(
            search_url,
            headers=headers,
            timeout=15
        )            
        data = response.json()        
        # 检查是否搜索成功
        if data.get('code') != 0:
            logger.warning(f"未找到文件: {file_name_with_ext}")
            return None       
        items = data.get('data', {}).get('InfoList', [])
        all_items.extend(items)
            
        logger.info(f"找到 {len(all_items)} 个匹配的搜索结果")
        # 3. 筛选出与文件名完全一致的结果（包含扩展名）
        exact_matches = []
        for item in all_items:
            # 确保item是字典类型且包含'FileName'字段，并且Type为0
            if isinstance(item, dict) and 'FileName' in item and item.get('Type') == 0:
                # 比较文件名（包含扩展名）是否完全匹配
                item_name = item['FileName']
                # 去掉扩展名后检查是否在目标文件名中存在，并且扩展名一致
                file_name_no_ext = file_name_with_ext.rsplit('.', 1)[0] if '.' in file_name_with_ext else file_name_with_ext
                item_ext = item_name.rsplit('.', 1)[1].lower() if '.' in item_name else ''
                target_ext = file_name_with_ext.rsplit('.', 1)[1].lower() if '.' in file_name_with_ext else ''
                if file_name_no_ext in item_name and item_ext == target_ext and not item.get('Trashed'):
                    logger.info(f"找到匹配: '{item_name}'")
                    exact_matches.append(item)
        logger.info(f"筛选出 {len(exact_matches)} 个与文件名一致的结果")
        # 4. 如果有多个匹配结果，返回文件大小最大的那个
        download_url = None
        if exact_matches:
            # 找到文件大小最大的项
            largest_file = max(exact_matches, key=lambda x: x.get('BaseSize', 0))
            file_id = largest_file.get('FileId')          
            s3_key_flag = largest_file.get('S3KeyFlag') 
            file_size = largest_file.get('Size') 
            etag = largest_file.get('Etag') 
            filename = largest_file.get('FileName')
            # 5. 直接获取下载直链
            logger.info(f"获取下载链接: {file_id}")
            download_url = get_downurl(client, f"123://{filename}|{file_size}|{etag}?{s3_key_flag}")
            url_cache[file_name_with_ext] = (file_id, download_url, current_time)
            return download_url
           
        if download_url == None:
            # 使用guessit获取标题名
            guess_result = guessit.guessit(cleaned_file_name)
            
            # 后备方案：优先使用空格分割，如果没有空格则使用点号分割
            if 'title' not in guess_result:
                if ' ' in cleaned_file_name:
                    first_part = cleaned_file_name.split(' ')[0]
                elif '.' in cleaned_file_name:
                    first_part = cleaned_file_name.split('.')[0]
                else:
                    first_part = cleaned_file_name
            else:
                if guess_result['type'] == 'episode':
                    # 从原始文件名中提取S01E05或s01e02格式的季数和集数（不区分大小写）
                    season_episode_match = re.search(r'S\d+E\d+', file_path, re.IGNORECASE)
                    if season_episode_match:
                        season_episode = season_episode_match.group()
                        first_part = guess_result['title'] + season_episode
                    else:
                        first_part = guess_result['title']
                else:
                    first_part = guess_result['title']
            print(first_part)
            logger.info(f"进行第二轮搜索，使用guessit提取的标题名: {first_part}")
            search_url_first_part = f"https://www.123pan.com/b/api/file/list/new?driveId=0&limit=100&next=0&orderBy=update_time&orderDirection=desc&parentFileId=0&trashed=false&SearchData={first_part}&Page=1&OnlyLookAbnormalFile=0&event=homeListFile&operateType=2&inDirectSpace=false"
            response_second = requests.get(
                search_url_first_part,
                headers=headers,
                timeout=15
            )
            data_second = response_second.json()
            if data_second.get('code') == 0:
                items_second = data_second.get('data', {}).get('InfoList', [])
                all_items=[]
                all_items.extend(items_second)
                logger.info(f"第二轮搜索找到 {len(items_second)} 个匹配的搜索结果")
                exact_matches = []
                for item in all_items:
                     # 确保item是字典类型且包含'FileName'字段，并且Type为0
                    if isinstance(item, dict) and 'FileName' in item and item.get('Type') == 0:
                        # 比较文件名（包含扩展名）是否完全匹配
                        item_name = item['FileName']
                        # 去掉扩展名后检查是否在目标文件名中存在，并且扩展名一致
                        file_name_no_ext = file_name_with_ext.rsplit('.', 1)[0] if '.' in file_name_with_ext else file_name_with_ext
                        item_ext = item_name.rsplit('.', 1)[1].lower() if '.' in item_name else ''
                        target_ext = file_name_with_ext.rsplit('.', 1)[1].lower() if '.' in file_name_with_ext else ''
                        if file_name_no_ext in item_name and item_ext == target_ext and not item.get('Trashed'):
                            logger.info(f"找到匹配: '{item_name}'")
                            exact_matches.append(item)
                logger.info(f"筛选出 {len(exact_matches)} 个与文件名完全一致的结果")
                # 4. 如果有多个匹配结果，返回文件大小最大的那个
                download_url = None
                if exact_matches:
                    # 找到文件大小最大的项
                    largest_file = max(exact_matches, key=lambda x: x.get('BaseSize', 0))
                    file_id = largest_file.get('FileId')          
                    s3_key_flag = largest_file.get('S3KeyFlag') 
                    file_size = largest_file.get('Size') 
                    etag = largest_file.get('Etag') 
                    filename = largest_file.get('FileName')
                    # 5. 直接获取下载直链
                    logger.info(f"获取下载链接: {file_id}")
                    download_url = get_downurl(client, f"123://{filename}|{file_size}|{etag}?{s3_key_flag}")
                    url_cache[file_name_with_ext] = (file_id, download_url, current_time)
                    return download_url
            else:
                logger.warning(f"第二轮搜索失败: {data_second.get('message', '未知错误')}")
                return None

        logger.warning(f"未找到文件: {file_name_with_ext}")
        return download_url
    except Exception as e:
        logger.error(f"搜索或获取下载链接过程中发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    # 测试get_download_url_by_path函数
    test_file_path = "“湾区升明月”2025大湾区电影音乐晚会 (2025) - 2160p.HDTV.HDR.H.265.10-bit.AC3 5.1.ts"
    
    try:
        print("\n===== 测试get_download_url_by_path函数 =====")
        print(f"测试文件路径: {test_file_path}")
        
        # 为搜索调用添加计时
        search_start_time = time.time()
        download_url = get_download_url_by_path_xiaohao(test_file_path)
        search_end_time = time.time()
        
        print(f"搜索完成，耗时: {search_end_time - search_start_time:.4f} 秒")
        
        # 打印找到的下载链接信息
        if download_url:
            print(f"找到匹配的文件并获取到下载链接：")
            print(f"下载链接: {download_url}")
        else:
            print("未找到与文件名完全匹配的结果")
        
    except Exception as e:
        print(f"搜索或获取下载链接过程中发生错误: {str(e)}")

