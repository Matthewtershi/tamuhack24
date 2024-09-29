FROM continuumio/miniconda3

RUN conda install -c conda-forge nceplibs-g2c grib2io herbie-data -y --solver classic
RUN pip install netCDF4 Flask flask-cors

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python", "flask-server/server.py" ]
