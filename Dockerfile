FROM continuumio/miniconda3

RUN conda install -c conda-forge nceplibs-g2c -y
RUN conda install -c conda-forge grib2io -y --solver classic
RUN pip install netCDF4

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python", "server/firedata.py" ]