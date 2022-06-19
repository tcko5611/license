#! /depot/Python-3.5.2/bin/python
import os
def createWorkerScript(worker):
    fileName = worker + '.sh'
    with open(fileName, 'w') as f:
        license = os.environ['LM_SERVER']
        xa = '/remote/tw_rnd1/ktc/license/CustomSim/xa'
        outdir = 'tmp'
        f.write('#! /bin/bash\n')
        f.write('export LM_SERVER=\'' + license + '\'\n')
        f.write('if [ $# -eq 0 ]\n')
        f.write('then\n')
        f.write('  ' + xa + ' -i ' + worker + ' -o ' + outdir + '/workers/' \
                + worker + '\n')
        f.write('else\n')
        f.write('  ' + xa + ' -i ' + worker + ' -o ' + outdir + '/workers/' \
                + worker + ' -t $1\n')
        f.write('fi\n')
    os.chmod(fileName, 0o755)
    

if __name__ == '__main__':
    a = [1, 2,3]
    b= a.copy()
    b[1] = 3
    print(a)
    print(b)

