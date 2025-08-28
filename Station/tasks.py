from celery import shared_task
import subprocess
from pathlib import Path

@shared_task(bind=True)
def run_ncl_script_task(self, script_path, dir_out, input_folder, domain, input_path, out_path, lat, lon, hour):
    try:
        cwd_path = Path(script_path).parent
        result = subprocess.run(
            ['bash', script_path, input_folder, domain, input_path, out_path, lat, lon, hour],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=cwd_path
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout.decode(),
            'stderr': result.stderr.decode()
        }
    except Exception as e:
        return {'error': str(e)}