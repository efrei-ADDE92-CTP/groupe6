import subprocess

url = 'http://localhost:5000/predict'

cmd = f'hey -n 10000 -c 100 -m POST {url}'
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if error:
    print(f'An error occurred: {error}')
else:
    print(output.decode('utf-8'))
