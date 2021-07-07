import hashlib
import requests

import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    return proof



def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess_hash)
    # return guess_hash[:3] == "000"
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    username = input('Please input an ID:')
    # f = open("my_id.txt", "r")
    # username = f.read()
    # print("ID is", username)
    # f.close()
    id_list = [username,]
    
    print('Commands:\n"mine": mine one coin\n"balance": display current balance\n"transactions": Display the list of all your transactions\n"id": Change your ID\n"q": Close miner')
    while True:
        cmd = input('->')
        if cmd == 'mine':
            pass
        elif cmd == 'balance':
            balance = 0
            r = requests.get(url=node + "/chain")
            data = r.json()
            for block in data['chain']:
                for transaction in block['transactions']:
                    if transaction['recipient'] in id_list:
                        balance += 1
            print(f'Current balance: {balance} coins')
            continue
        elif cmd == 'transactions':
            r = requests.get(url=node + '/chain')
            data = r.json()
            for block in data['chain']:
                for transaction in block['transactions']:
                    if transaction['recipient'] in id_list or transaction['sender'] in id_list:
                        print(transaction)
            continue
        elif cmd == 'id':
            username = input('Please choose a new id \n->')
            id_list.append(username)
            continue
        elif cmd == 'q':
            break
        else:
            print(f'{cmd} is not a valid command')
            continue
        proof_counter = 0
        coins_mined = 0
        # Run forever until interrupted
        while True:
            r = requests.get(url=node + "/last_block")
            # Handle non-json response
            try:
                data = r.json()
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(r)
                break

            # TODO: Get the block from `data` and use it to look for a new proof
            block = data['block']
            new_proof = proof_of_work(block)
            proof_counter = new_proof
            # print(new_proof)

            # When found, POST it to the server {"proof": new_proof, "id": id}
            post_data = {"proof": new_proof, "id": username}


            r = requests.post(url=node + "/mine", json=post_data)
            data = r.json()

            # TODO: If the server responds with a 'message' 'New Block Forged'
            if data['message'] == "New Block Forged":
                coins_mined += 1
                print(f'Coins mined: {coins_mined}')
                break
            else:
                print(data['message'])
                break
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.
