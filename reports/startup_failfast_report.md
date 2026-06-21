# Startup Fail-Fast Report
- **Simulated Missing Artifact**: model.pkl
- **Exit Code**: 3
- **Startup Log Output**:
```text
Failed to load ML artifacts: [Errno 2] No such file or directory: 'D:\\SEMESTER 6\\Pembelajaran Mesin\\UAS\\UAS_MachineLearning_Diabetes\\models\\artifacts\\model.pkl'
INFO:     Started server process [30664]
INFO:     Waiting for application startup.
ERROR:    Traceback (most recent call last):
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\backend\startup\load_artifacts.py", line 20, in load_all_artifacts
    ArtifactStore.model = joblib.load(os.path.join(base_dir, 'model.pkl'))
                          ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\.venv\Lib\site-packages\joblib\numpy_pickle.py", line 735, in load
    with open(filename, "rb") as f:
         ~~~~^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'D:\\SEMESTER 6\\Pembelajaran Mesin\\UAS\\UAS_MachineLearning_Diabetes\\models\\artifacts\\model.pkl'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\.venv\Lib\site-packages\starlette\routing.py", line 638, in lifespan
    async with self.lifespan_context(app) as maybe_state:
               ~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "C:\Python314\Lib\contextlib.py", line 214, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\.venv\Lib\site-packages\fastapi\routing.py", line 232, in merged_lifespan
    async with original_context(app) as maybe_original_state:
               ~~~~~~~~~~~~~~~~^^^^^
  File "C:\Python314\Lib\contextlib.py", line 214, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\backend\main.py", line 11, in lifespan
    load_all_artifacts()
    ~~~~~~~~~~~~~~~~~~^^
  File "D:\SEMESTER 6\Pembelajaran Mesin\UAS\UAS_MachineLearning_Diabetes\backend\startup\load_artifacts.py", line 33, in load_all_artifacts
    sys.exit(1)
    ~~~~~~~~^^^
SystemExit: 1

ERROR:    Application startup failed. Exiting.
```
- **Status**: PASS
