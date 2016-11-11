# doctor
POC: Red Thomas <red.thomas@redknightllc.com>

doctor.py - Script that generates general traffic.

donna.py  - Companion script that generates traffic from separate configuration
            file.

## Scope
Doctor and DoctorDonna are designed to generate test data for an Elastic Stack
environment.  The idea is to use Doctor to generate bulk data over time, while
Donna generates a subset of unique data which should be identifiable using the
significant terms search in Elasticsearch or Kibana.

Both scripts look to json-formatted files for basic configuration data used in
the generation of test documents.

For the test case, I decided to use general system health information.  I wanted
to use something that might eventually be useful, and I wanted a template with
multiple arrays of data in it so that I could play with the split and clone
filters in Logstash.
