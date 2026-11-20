"""Run every notebook cell and regenerate its tables, figures and PDF report."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from pathlib import Path
import time
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    path = root / 'Castle_Doctrine_Replication.ipynb'
    notebook = nbformat.read(path, as_version=4)
    shell = InteractiveShell.instance()
    started = time.perf_counter()
    count = 0
    for cell in notebook.cells:
        if cell.cell_type != 'code':
            continue
        count += 1
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=True)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(f'Cell {count} failed:\n{captured.stdout}\n{captured.stderr}') from (result.error_before_exec or result.error_in_exec)
        cell.execution_count = count
        cell.outputs = []
        if captured.stdout:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
        if captured.stderr:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print(f'Completed {count} code cells in {time.perf_counter() - started:.1f} seconds.')
    print('Report: Castle_Doctrine_Replication.pdf')
    print('Tables and figures: castle_doctrine_run/output/')

if __name__ == '__main__':
    main()
