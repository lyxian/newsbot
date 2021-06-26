# Place all secrets in .config of base directory, with the naming format of <appName>.json

from cryptography.fernet import Fernet
import os

def writeBytes(filename, data):
    with open(filename, 'wb') as file:
        print(f'Saved to {filename}')
        file.write(data)

def start():
    dir_prefix = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    key = Fernet.generate_key()
    filenames = [filename for filename in os.listdir(os.path.join(dir_prefix, '.config')) if "json" in filename]
    
    try:
        writeBytes(dir_prefix + '/.config/key.txt', key)
        env_msg = {
            'KEY': f'\nexport KEY="{key.decode()}"'
        }
        for filename in filenames:
            appName = filename.split('.json')[0].upper()
            with open(dir_prefix + f'/.config/{filename}', 'rb') as file:
                data = file.read()
            encrypted_data = Fernet(key).encrypt(data)
            writeBytes(dir_prefix + f'/.config/secret_{appName.lower()}.txt', encrypted_data)
            print(f'Encrypting {appName} successful...')
            env_msg[f'{appName}_KEY'] = f'\nexport {appName}_KEY="{encrypted_data.decode()}"'

        # Set ENV
        with open(dir_prefix + '/.venv/bin/activate', 'a') as file:
            for msg, code in env_msg.items():
                file.write(code)
                print(f'{msg} set successfully')
            print('Reactivate venv to use new env...')
    except Exception as err:
        print(f'Encryption failed...\n{err}\nTry again...')

if __name__ == '__main__':
    start()