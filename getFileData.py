from selenium import webdriver
from selenium.webdriver.common.by import By

inputStr=input("输入fil节点ID：")

if inputStr=='':
    print("节点ID不能为空")
else:
    driver=webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://filscan.io/address/miner?address="+inputStr)
    data={}
    data['fil_balance']=driver.find_element(By.CLASS_NAME,value='num').text
    data['available'] = driver.find_element(By.CLASS_NAME, value='available').text
    data['pledged']=driver.find_element(By.CLASS_NAME,value='pledged').text
    data['deposits']=driver.find_element(By.CLASS_NAME,value='deposits').text
    data['reward']=driver.find_element(By.CLASS_NAME,value='reward').text
    data['power']=driver.find_element(By.XPATH,value='//div[@class="left font-20 font-400 text flex align-center"]').text
    data['total_reward']=driver.find_element(By.XPATH,value='//div[contains(text(),"总奖励: ")]/following-sibling::div[1]').text
    data['total_all_status']=driver.find_element(By.XPATH,value='//div[contains(text(),"扇区状态: ")]/following-sibling::div[1]/span').text
    data['total_used_status']=driver.find_element(By.XPATH,value='//div[contains(text(),"扇区状态: ")]/following-sibling::div[1]/span[@class="proving"]').text
    data['total_fault_status'] = driver.find_element(By.XPATH,value='//div[contains(text(),"扇区状态: ")]/following-sibling::div[1]/span[@class="fault"]').text
    data['total_pre_status'] = driver.find_element(By.XPATH,value='//div[contains(text(),"扇区状态: ")]/following-sibling::div[1]/span[@class="pre"]').text
    data['power_add_num']=driver.find_element(By.XPATH,value='//div[@class="content-growth"]/div[@class="growth-item"]/div[@class="value"]').text
    print(f'账户余额: {data.get("fil_balance")}')
    print(f'{data.get("available")}')
    print(f'{data.get("pledged")}')
    print(f'{data.get("deposits")}')
    print(f'{data.get("reward")}')
    print(f'有效算力:{data.get("power")}')
    print(f'总奖励: {data.get("total_reward")}')
    print(f'扇区状态: {data.get("total_all_status")}')
    print(f'扇区状态: {data.get("total_used_status")}')
    print(f'扇区状态: {data.get("total_fault_status")}')
    print(f'扇区状态: {data.get("total_pre_status")}')
    print(f'算力增量: {data.get("power_add_num")}')

    driver.close()
#     f021479    f070932      f01231   f015932    f01466173

