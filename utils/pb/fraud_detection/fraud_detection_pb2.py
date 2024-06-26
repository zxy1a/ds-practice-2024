# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fraud_detection.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x0f\x66raud_detection\"y\n\x0bVectorClock\x12:\n\x07\x65ntries\x18\x01 \x03(\x0b\x32).fraud_detection.VectorClock.EntriesEntry\x1a.\n\x0c\x45ntriesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\"\x80\x01\n\x14\x43heckUserDataRequest\x12\x0f\n\x07orderID\x18\x01 \x01(\t\x12#\n\x04user\x18\x02 \x01(\x0b\x32\x15.fraud_detection.User\x12\x32\n\x0cvector_clock\x18\x03 \x01(\x0b\x32\x1c.fraud_detection.VectorClock\"m\n\x15\x43heckUserDataResponse\x12\x10\n\x08is_fraud\x18\x01 \x01(\x08\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x32\n\x0cvector_clock\x18\x03 \x01(\x0b\x32\x1c.fraud_detection.VectorClock\"\x84\x01\n\x15\x46raudDetectionRequest\x12\x0f\n\x07orderID\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x02 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x03 \x01(\t\x12\x32\n\x0cvector_clock\x18\x04 \x01(\x0b\x32\x1c.fraud_detection.VectorClock\"n\n\x16\x46raudDetectionResponse\x12\x10\n\x08is_fraud\x18\x01 \x01(\x08\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x32\n\x0cvector_clock\x18\x03 \x01(\x0b\x32\x1c.fraud_detection.VectorClock\"6\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x03 \x01(\t2\xe8\x01\n\x0e\x46raudDetection\x12l\n\x17\x43heckCreditCardForFraud\x12&.fraud_detection.FraudDetectionRequest\x1a\'.fraud_detection.FraudDetectionResponse\"\x00\x12h\n\x15\x43heckUserDataForFraud\x12%.fraud_detection.CheckUserDataRequest\x1a&.fraud_detection.CheckUserDataResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VECTORCLOCK_ENTRIESENTRY']._options = None
  _globals['_VECTORCLOCK_ENTRIESENTRY']._serialized_options = b'8\001'
  _globals['_VECTORCLOCK']._serialized_start=42
  _globals['_VECTORCLOCK']._serialized_end=163
  _globals['_VECTORCLOCK_ENTRIESENTRY']._serialized_start=117
  _globals['_VECTORCLOCK_ENTRIESENTRY']._serialized_end=163
  _globals['_CHECKUSERDATAREQUEST']._serialized_start=166
  _globals['_CHECKUSERDATAREQUEST']._serialized_end=294
  _globals['_CHECKUSERDATARESPONSE']._serialized_start=296
  _globals['_CHECKUSERDATARESPONSE']._serialized_end=405
  _globals['_FRAUDDETECTIONREQUEST']._serialized_start=408
  _globals['_FRAUDDETECTIONREQUEST']._serialized_end=540
  _globals['_FRAUDDETECTIONRESPONSE']._serialized_start=542
  _globals['_FRAUDDETECTIONRESPONSE']._serialized_end=652
  _globals['_USER']._serialized_start=654
  _globals['_USER']._serialized_end=708
  _globals['_FRAUDDETECTION']._serialized_start=711
  _globals['_FRAUDDETECTION']._serialized_end=943
# @@protoc_insertion_point(module_scope)
