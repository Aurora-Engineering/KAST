# Knowledge Aquisition and Synthesis Tool
from kast.src.runtime.core import KastRuntime


def main():
	runtime = KastRuntime('kast/config/pybullet_config.ini')
	runtime.execute('both')

if __name__ == '__main__':
	main()












