import datetime as dt
from pathlib import Path


def generate_data_dir(
        root_dir: Path,
        dataset_name: str,
        time_key: dt.datetime
    ):
    # 构建目录
    partition_dir = root_dir / dataset_name / \
                        f"{time_key.year}" / \
                        f"{time_key.month:02d}" / \
                        f"{time_key.day:02d}"  
    return partition_dir

def generate_time_tag(delta: str="1h"):
    if delta == "1d":
        delta_time = dt.timedelta(hours=24)
        time_tag = "%Y%m%d"
    else:
        delta_time = dt.timedelta(hours=1)
        time_tag = "%Y%m%d_%H"
    return delta_time, time_tag