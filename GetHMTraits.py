
from web3 import Web3
import json
import time
import asyncio
#import pandas

infuraAPIKey = 'insert your infura api key here'#insert your infura api key here
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+ infuraAPIKey))

t_id1 = 0
TotalMintCount = 16384
singleItem =  0 #16383 # change this to tokenid if you only want to output one value
output=[]
tokenid = 2702


# hashmasks contract and abi which was obtained via an api call to etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0x185c8078285a3de3ec9a2c203ad12853f03c462d&apikey=INSERT_YOUR_API_KEY_HERE
contract_address='0x185c8078285a3de3ec9a2c203ad12853f03c462d'
abi = json.loads('[{\"inputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[],\"name\":\"DATASTORE_CONTRACT\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"MASKS_CONTRACT\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"maskId\",\"type\":\"uint256\"}],\"name\":\"getIPFSHashOfMaskId\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"ipfsHash\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"maskId\",\"type\":\"uint256\"}],\"name\":\"getTraitsOfMaskId\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"character\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"mask\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"eyeColor\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"skinColor\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"item\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"maxMasksSupply\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"startingIndexFromMasksContract\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"}]')

contract_address= Web3.toChecksumAddress(contract_address)
contract = w3.eth.contract(address=contract_address, abi=abi)

traitTypes = contract.functions.getTraitsOfMaskId(tokenid)
## I think the trait types are all the same for each token if not then need to call
## this for each token


########single call to get traits function

# traits = contract.functions.getTraitsOfMaskId(tokenid).call()
# j={"tokenid":tokenid}
# for t in range(len(traits)):
#     #traitTypes[t]
#     d={}
#     i =  [{"tokenid":tokenid}] + traitTypes.abi["outputs"]
#     d[ traitTypes.abi["outputs"][t]["name"]] = traits[t]
#     j.update(d)
# print(i)
######### can comment everything out below to use this

def pingAPI(url):
    traits = contract.functions.getTraitsOfMaskId(url).call()
    j={"tokenid":url}
    for t in range(len(traits)):
        d={}        
        d[ traitTypes.abi["outputs"][t]["name"]] = traits[t]
        j.update(d)

    return j


async def loopAPIcalls (loop, i):
    filesInternal = []        
    
    await loop.run_in_executor(None, lambda:filesInternal.append( pingAPI(i)))

    return filesInternal
    
def export (files):
   
    #df = pandas.DataFrame(files)
    #df.to_csv('ab_out160' + str(time.time()).split('.')[0] + '.csv')

    with open('NFTTraits' + str(time.time()).split('.')[0] + '.json', "w") as f:
        json.dump(files, f , sort_keys=True, default=str)
 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if singleItem > 0: # as in has a token id
        output.append(pingAPI(singleItem))

    else:        
        results =  loop.run_until_complete(
            asyncio.gather(*(loopAPIcalls(loop,i) for i in range(t_id1,TotalMintCount) ))            
        )
        for f in results:        
            output.append(f)
     
    export (output)