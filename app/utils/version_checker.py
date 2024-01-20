from asyncio.subprocess import create_subprocess_shell
from subprocess import PIPE


START_VERSION = [0,0,0]
START_COMMIT = None

async def _read_commits() -> dict[str,str]:
	process = await create_subprocess_shell('git log --pretty=oneline',stdout=PIPE)
	commits = reversed((await process.stdout.read()).decode().splitlines())
	return {commit.split(' ',1)[0]:commit.split(' ',1)[1] for commit in commits}

async def _find_start_commit(commits:dict[str,str]) -> dict[str,str]:
	if START_COMMIT is None: return commits
	for commit in commits.copy():
		if commit == START_COMMIT:
			break
		del commits[commit]
	return commits
	
def calculate_version(commits:dict[str,str]) -> list[int]:
	version = START_VERSION.copy()
	for message in commits.values():
		match message.strip().lower():
			case 'major version bump'  : version = [version[0]+1,0,0]
			case 'minor version bump'  : version = [version[0],version[1]+1,0]
			case 'patch version bump'|_: version[2] += 1
	return version

async def get_version() -> str:
	commits = await _read_commits()
	filtered_commits = await _find_start_commit(commits)
	version = calculate_version(filtered_commits)
	return '.'.join([str(v) for v in version])

if __name__ == '__main__':
	from asyncio import run
	print(run(get_version()))