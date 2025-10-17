import logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import asyncio
import json
from quark import QuarkUcSDK
import base64
import time
import asyncio
import re

# 从分享URL中提取分享ID和密码
def extract_share_info_from_url(share_url):
    # 匹配分享URL格式，提取分享ID
    share_id_match = re.search(r'/s/([a-zA-Z0-9]+)', share_url)
    if not share_id_match:
        raise ValueError(f"无效的分享URL: {share_url}")
    share_id = share_id_match.group(1)
    # 提取密码（如果有）
    password_match = re.search(r'pwd=([a-zA-Z0-9]+)', share_url)
    password = password_match.group(1) if password_match else ""
    return share_id, password

def sanitize_string(s: str) -> str:
    """
    清理字符串中的无效Unicode字符，以避免编码错误。
    参数:
        s (str): 待处理的字符串。
    返回:
        str: 清理后的字符串。
    """
    # 将字符串编码为utf-8字节，将无效字符替换为'?'
    # 然后再将字节解码回字符串
    return s.encode('utf-8', errors='replace').decode('utf-8')

def export_share_info(share_url, cookie=""):
    json_data = {
            "usesBase62EtagsInExport": False,
            "files": [],
        }
    async def main(batch_size: int = 50):
        start_time = time.time()
        my_cookie = cookie  
        # 从URL中提取分享ID和密码
        try:
            code, password = extract_share_info_from_url(share_url)
            logger.info(f"从URL提取到分享ID: {code}，密码: {password if password else '无'}")
        except ValueError as e:
            logger.error(f"错误: {e}")
            return
        file_name = "share.json"
        async with QuarkUcSDK(cookie=my_cookie) as quark:
            # 1. 获取分享信息
            share_info_result = await quark.get_share_info(code, password)
            logger.info("--- 正在获取分享信息 --- ")
            
            if share_info_result.get("code") == 0:
                stoken = share_info_result["data"]["stoken"]
                
                # 2. 收集所有文件信息
                logger.info(f"--- 正在收集文件信息 --- ")
                files_info = []
                file_mapping = {}
                
                async for file_info in quark.get_share_file_list(
                    code=code,
                    passcode=password,
                    stoken=stoken,
                    dir_id=0,
                    is_get_folder=False,
                    is_recursion=True,
                ):
                    # 存储文件基本信息
                    file_base = {
                        "size": file_info["size"],
                        "path": sanitize_string(file_info["RootPath"].lstrip('/')),
                    }
                    file_mapping[file_info["fid"]] = file_base
                    # 存储用于批量获取MD5的信息
                    files_info.append((file_info["fid"], file_info["share_fid_token"]))
                    
                total_files = len(files_info)
                logger.info(f"--- 已收集 {total_files} 个文件信息，开始批量获取MD5值 (批次大小: {batch_size}) --- ")
                
                # 3. 批量获取MD5值
                if total_files > 0:
                    md5_results = await quark.batch_send_create_share_download_request(
                        code=code,
                        pwd=password,
                        stoken=stoken,
                        file_info_list=files_info,
                        batch_size=batch_size
                    )
                    
                    # 4. 处理结果
                    logger.info("--- 正在处理结果并生成秒传 --- ")
                    for fid, file_base in file_mapping.items():
                        if fid in md5_results and 'md5' in md5_results[fid]:
                            md5_info = md5_results[fid]
                            if '==' in md5_info['md5']:    
                                md5 = base64.b64decode(md5_info['md5']).hex()
                            else:    
                                md5 = md5_info['md5']
                            file_base["etag"] = md5
                            json_data["files"].append(file_base)
                    
                # 5. 写入JSON文件
                #with open(file_name, "w", encoding='utf-8') as f:
                    #json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                #print(f"--- 成功生成JSON文件: {file_name}，共 {len(json_data['files'])} 个文件 --- ")
            else:
                logger.error(f"--- 获取分享信息失败，错误码: {share_info_result.get('code')} --- ")
        
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"--- 程序运行完成 --- ")
        logger.info(f"总耗时: {execution_time:.2f} 秒")
    # 运行异步函数
    asyncio.run(main())
    return json_data

# 如果直接运行此脚本
if __name__ == "__main__":
    share_url = "https://pan.quark.cn/s/c094a3711bcc"
    cookie = "_qk_bx_ck_v1=eyJkZXZpY2VJZCI6ImVDeSNBQU9vVDZndkhOTzBOL1paNlBEcjEvL1B6cWxTRU5tSXBCRkVKakthaEczdmVDMzhQbVNXaVNlUy9wTXFtSnAyUFU0PSIsImRldmljZUZpbmdlcnByaW50IjoiYzE0NWNkY2U1ZTYyODUwMWU3NDMwYTAyZTY3YjhiNGYifQ==; b-user-id=9929ebb9-0dc2-5ed5-abac-6b84b193e8c9; __wpkreporterwid_=d13832ca-d23d-4242-96fc-5d4cc2fe78b7; _UP_A4A_11_=wb9cb17952bb43fe8b4f3695eff09cdd; b-user-id=9929ebb9-0dc2-5ed5-abac-6b84b193e8c9; ctoken=MF6J0Q81r_ijS0nNy6i8Rxdr; web-grey-id=80f1ce41-95a4-4e83-a08b-df6951fbac96; web-grey-id.sig=EIB_ia64X9AP-Nyd-aSj3klEUTZRz8B_sR_JC3G_8YY; grey-id=e04a0571-d3fd-b80e-2759-bce0e9ca17d9; grey-id.sig=M9UApHT-QexIN6gtYxrXESFrsEMUmgfUTu7CUGukAlc; isQuark=true; isQuark.sig=hUgqObykqFom5Y09bll94T1sS9abT1X-4Df_lzgl8nM; __sdid=AAR18dAzGeXddKEvUjPHmcnz76Iom8plLlP7zUd/BcOr0W5CEDTkwiy0ocATiu28duDuKHQXVnPkAGXKvZHnXydoIwOL48AMq7fK99aF46dx1w==; _UP_D_=pc; xlly_s=1; __chkey=; __pus=1a099988568d7709539e6d50835cbdd7AASEqIoKZbQx6jCw49mNdNcecnB54KyEXwt24Ow1+NN5ytPT051rMt4Q95RottoHhdZeLZkN9keENVjrHQY5QOSM; __kp=9e9940c0-949f-11f0-bd58-8bb2451e1ac6; __kps=AARQDre99j4kWTEzt1WZFgeD; __ktd=eaaqz0znDaxM+jVdRG78ug==; __uid=AARQDre99j4kWTEzt1WZFgeD; isg=BM_PCpzo-wqyf__Fe3VclXrRXmPZ9CMW4vdHhOHZTD5FsOSy6MQUZtvjsuAOyPuO; tfstk=g46jDU2l2q0jeg1pGdrrNmYrfhps5uyeHctOxGHqXKpAXd_Wznl4iCz1NNQykxJvMhMRWNgxMrcxCd_eSEpNgE-OPGQYmhrcC_D1xGX4mdrDnivMByzULRscmdVeisFYYLhJvgK9X7RA-NgneyzUL8Px2dab8N73hqAJjUKvXCKYVQKMDdK9DdEWyhtn6qQ9BuZWbHH9XIKO2LK2XdLOWdE52Ux6BnQ9BusJrhhky4taGhIbv7MyRKoucaYSBABW2PYCc-k2A9-XGeIAhADgvnOXJiL7kX0hBQIM1OmiCCsAtNxdkqUeiGC5Pn9_UjpdV1QBqteEl3fV2M8RADHdvKt69ddSXAIWnUARepeKP3fR01BclcM9mtWe1eA7XAAwe9Rd9ZigxgpvXNAhQyDDkGIhK6JQUjpdV1QC1g7ZLe9TvfiWtAtW8uZSsfX3B_avmz-A7IKkDJr7V4GMM3xW8uZSsfAvqnCUVugSs; __puus=df4074814eb2c70631be5ab02bf2a9b2AARpAPoHtOuWl5F5UVWt6nL6nBUMVsUw9Go4NYcEZJzE2P7xx4JeJ8YhweFptj29Cex6g+vTIBJCrp2XYticR3b3104076oq1M3YOiydk9hZBntbeSUiT2Fu1Hu85i6FspPc0VnxlH6i5Cu9sU3F1axhMq03GAtGs/nKQiKVIfw/H+HGkiHMqCERIbKJxSf6dFYM1tzjzfx3VK5A/freUU3W"
    print(export_share_info(share_url, cookie))
