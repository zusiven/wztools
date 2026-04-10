import warnings
import datetime as dt

from pathlib import Path
from . import generate_data_dir, generate_time_tag


def generate_data_path(
        root_dir: Path,
        dataset_name: str,
        special_key: str,
        time_key: dt.datetime,
        suffix: str="parquet",
        delta: str="1h"
):
    """
    根据时间点和数据集名称，生成 [suffix] 文件的标准存储路径 (包含文件名)。
    结构: ./root_dir/dataset_name/Y/M/D/YYYYMMDD_HH_[special_key].[suffix]
    Args:
        - root_dir (pathlib.Path): 数据池的根目录。
        - dataset_name (str): 数据集的名称 (e.g., 'ERA5_Hourly')。
        - time_key (datetime.datetime): 数据的时间点。
        - special_key (str): 可选的特殊标识符，如 'v2'。
        - delta_hour: 1h 1d
    """
    partition_dir = generate_data_dir(root_dir, dataset_name, time_key)
    partition_dir.mkdir(exist_ok=True, parents=True)

    _, time_tag = generate_time_tag(delta)

    # 构建文件名
    time_part = time_key.strftime(time_tag)
    file_stem = f"{time_part}_{special_key}"
    file_name = f"{file_stem}.{suffix}"

    return partition_dir / file_name

def get_data_paths(
        root_dir: Path,
        dataset_name: str,
        special_key: str,
        start_time: dt.datetime,
        end_time: dt.datetime,
        suffix: str="parquet",
        delta: str="1h",
):
    """
    通过精准的时间分区索引，快速获取时间范围内的 suffix 文件路径列表。
    Args:
        - root_dir (pathlib.Path): 数据池的根目录。
        - dataset_name (str): 数据集的名称 (e.g., 'ERA5_Hourly')。
        - special_key (str): 可选的特殊标识符，如 'v2'。
        - start_time (dt.datetime): 起始时间
        - end_time (dt.datetime): 结束时间
        - delta_hour: 1h 1d
    """
    # 初始化结果列表
    file_paths = []
    
    delta_time, time_tag = generate_time_tag(delta)
    processed_time_points = set()
    current_time = start_time
    while current_time <= end_time:
        partition_dir = generate_data_dir(root_dir, dataset_name, current_time)
        # 步骤 2: 仅处理尚未处理的日期
        if current_time not in processed_time_points:
            file_path = partition_dir / f"{current_time.strftime(time_tag)}_{special_key}.{suffix}"

            if file_path.exists():
                file_paths.append(file_path)

        processed_time_points.add(current_time)
        current_time += delta_time

    if len(file_paths) == 0:
        warnings.warn(f"No {special_key} files found in [{start_time}, {end_time}]", UserWarning)

    return file_paths

def combine_daily_data(input_files: list[Path], output_path: Path, suffix: str="parquet"):
    """
        suffix: parquet | csv
    """
    import polars as pl
    if suffix == "csv":
        df = pl.scan_csv(input_files).collect()
        df.write_csv(output_path)
    else:
        df = pl.scan_parquet(input_files).collect()
        df.write_parquet(output_path)
    