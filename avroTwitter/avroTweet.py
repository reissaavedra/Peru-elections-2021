import avro.schema
from avro.datafile import DataFileReader,DataFileWriter
from avro.io import DatumReader,DatumWriter
import os

path_schema = './../schema'
path_avro_file = './../avro'

schema = avro.schema.parse(
    open(os.path.join(path_schema,'schemaTwitter.avsc'), 'rb').read()
)

writer = DataFileWriter(
    open(os.path.join(path_avro_file, 'tweet.avro'), 'wb'), DatumWriter(), schema
)

writer.append({'name': 'Alyssa','favorite_number': 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.close()


reader = DataFileReader(
    open(os.path.join(path_avro_file, 'tweet.avro'), 'rb'), DatumReader()
)

for t in reader:
    print(t)
reader.close()
