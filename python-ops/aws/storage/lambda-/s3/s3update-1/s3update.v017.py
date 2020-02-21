# Compare a file on S3 to see if we have the latest version
# If not, upload it and invalidate
import hashlib
import os
import sys
import threading
import time
import logging
import boto3
from optparse import OptionParser
from datetime import datetime
from time import gmtime, strftime

try:
    import yaml
except ImportError as ie:
    LIB_MAP = {'yaml': 'PyYAML'}
    m = ie.message
    missing_mod = m[m.rfind(" "):].strip()
    print("error: missing python module '%s' (please install manually)" % missing_mod)
    print("  use: pip install %s" % LIB_MAP.get(missing_mod, missing_mod))
    sys.exit(-1)


AWS_COPY_YAML_FILE = 'copy.yml'
CFG_KEY_SOURCE = 'source'
CFG_KEY_DEST = 'destination'
LOG_FILE_LOC = 's3update/'
s3 = boto3.resource('s3')
client = boto3.client('s3')


ts = strftime("%d-%b-%Y-%H-%M-%S", gmtime())
log_file_name = '{}-upload-status.log'.format(ts)
logging.basicConfig(
        filename=log_file_name,
        filemode='wb+',
        level=logging.INFO,
)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
tabStr = '         '
less = '      '
outstr = "Pxn_yr"+ tabStr + "pxn_mo" + less +  "pxn_dy" + less +"pxn_hr"+ less+"filename"+"\t\t"+ tabStr+"md5"
logging.info(outstr)


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._mod_time = time.localtime(os.path.getmtime(filename))
        self._total_size = float(os.path.getsize(filename))
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            transfered = ("%.0fkb" % (bytes_amount / 1000)).rjust(6)
            total = ("%.0fkb" % (self._total_size / 1000)).rjust(6)
            mt = time.strftime("%b %d  %H:%M", self._mod_time)
            sys.stdout.write("\ruploading  %s  %s  %s  %s" % (
                             self._filename, total, mt, transfered))
            sys.stdout.flush()


def error(msg, and_exit=True):
    # print("ERROR: %s" % msg)
    if and_exit:
        sys.exit(-1)


def get_upload_control_data(yaml_file):
    if not os.path.isfile(yaml_file):
        error("copy control file not exists: %s" % yaml_file)
    result = []
    with open(yaml_file) as f:
        y = yaml.load(f)
        for key in [CFG_KEY_SOURCE, CFG_KEY_DEST]:
            if key not in y:
                error("missing config entry '%s' in '%s'" % (key, yaml_file))
        sources = y[CFG_KEY_SOURCE]
        targets = y[CFG_KEY_DEST]
        '''if len(sources) != len(targets):
            error("mismatching length of config '%s (%s)' and '%s (%s)'" % (
                CFG_KEY_SOURCE, len(sources), CFG_KEY_DEST, len(targets)))'''
        for i, source in enumerate(sources):
            result.append((source, targets[i]))
    return result


# Shortcut to MD5
def get_md5(filename):
    f = open(filename, 'rb')
    m = hashlib.md5()
    while True:
        data = f.read(10240)
        if len(data) == 0:
                break
        m.update(data)
    return m.hexdigest()


def to_uri(filename, subpath):
    name = os.path.basename(filename)
    if subpath:
        return "%s/%s" % (subpath, name)
    return name


def get_values(pxn_string):
    value = filter(lambda x: 'pxn' in x, pxn_string.split("/"))
    fl = []
    for v in value:
        fl.append(v.split('=')[1])
    return fl


def upload(src_dir, bucket_target):
    # Split bucket target into a bucket_name and an optional subpath within the bucket
    # for the uploading files.
    if bucket_target.startswith("/"):
        bucket_target = bucket_target[1:]
    bucket_name = bucket_target.split('/')[0]
    subpath = "/".join([p for p in bucket_target.split('/')[1:] if p])
    assert os.path.isdir(src_dir), "Source directory '%s' not exists" % src_dir
    # Connect to S3 and get bucket
    bucket = s3.Bucket(bucket_name)
    # Assemble a list of all files from the given source directory
    files = []
    for root, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            outfile = src_dir+"/"+filename
            fl = get_values(bucket_target)
            logging.info(
                "Pxn_yr={} - pxn_mo={} - pxn_dy={} - pxn_hr={} - {} - md5 - {}".format(
                    fl[0], fl[1], fl[2], fl[3], filename, get_md5(outfile)))
            files.append(os.path.join(root, filename))

    # Compare them to S3 checksums
    files_to_upload = []
    for f in files:
        key = to_uri(f, subpath)
        objs = list(bucket.objects.filter(Prefix=key))

        if len(objs) > 0 and objs[0].key == key:
            # assert len(objs) == 0, "Too many objects found with key '%s'" % key
            # check MD5
            md5 = get_md5(f)
            etag = objs[0].e_tag.strip('"').strip("'")
            if etag != md5:
                # print(f + ": " + md5 + " != " + etag)
                files_to_upload.append(f)
        else:
            # new file, upload
            files_to_upload.append(f)
    # Upload + invalidate the ones that are different
    for filename in files_to_upload:
        uri = to_uri(filename, subpath)
        extra_args = {'StorageClass': 'STANDARD_IA'}
        value = filename.split('/')[-1]
	print "uploading", filename
        s3.meta.client.upload_file(filename, bucket_name, uri,
                                   ExtraArgs=extra_args,
                                   Callback=ProgressPercentage(f))
        print("")
    return files_to_upload


def lambda_handler(event, context):
    """AWD Lambda handler function."""
    uploaded_files = []
    for (source, target) in get_upload_control_data(AWS_COPY_YAML_FILE):
        uploaded_files.extend(upload(source, target))

    if not uploaded_files:
        return "No files uploaded"
    return "Uploaded %s file(s)" % len(uploaded_files)


def get_bucket_name(bucket_target):
    if bucket_target.startswith("/"):
        bucket_target = bucket_target[1:]
    bucket_name = bucket_target.split('/')[0]
    return bucket_name


def get_prefix(bucket_target):
    value = bucket_target.split('/')
    value.pop(0)
    prefix_str = '/'.join(value)
    return prefix_str


def get_destination_filenames(yaml_file):
    if not os.path.isfile(yaml_file):
        error("copy control file not exists: %s" % yaml_file)
    result = []
    with open(yaml_file) as f:
        y = yaml.load(f)
        for key in [CFG_KEY_SOURCE, CFG_KEY_DEST]:
            if key not in y:
                error("missing config entry '%s' in '%s'" % (key, yaml_file))
        targets = y[CFG_KEY_DEST]
        for i, source in enumerate(targets):
            result.append(targets[i])
    return result


def delete_files(target_source):
    bucket_name = get_bucket_name(target_source)
    prefix = get_prefix(target_source)
    value = s3.meta.client.list_objects(Bucket=bucket_name, Prefix=prefix)
    for x_key in value.get('Contents'):
        del_key = x_key.get('Key')
        # delete this key in s3 object
        response = client.delete_object(Bucket=bucket_name, Key=del_key)


def create_dirs(create_dir):
    for dirs in create_dir:
        bucket_name = get_bucket_name(dirs)
        prefix = get_prefix(dirs)
        print "creating dirs..\t", prefix
        data = ''
        # s3.meta.client.upload_file(prefix, bucket_name, prefix)
        s3.Bucket(bucket_name).put_object(Key=prefix, Body=data)
        # response = client.put_object(Bucket=bucket_name, Key=prefix)


def put_log_file():
    bucket_name = 'dev-log-3'
    current_time = datetime.today().strftime('%Y-%m-%d')
    final_key = LOG_FILE_LOC + current_time
    upload_file_name = os.getcwd()+"/"+log_file_name
    uri = final_key+"/"+log_file_name
    response = s3.meta.client.upload_file(
        upload_file_name, bucket_name, uri)


def main():
    """ Main method used from commandline."""
    opt_parser = OptionParser()
    opt_parser.add_option(
        "-u", "--filePath", dest="uploadfilepath",
        help="Upload files to bucket",
        default=False)
    opt_parser.add_option(
        "-d", "--bucket",
        dest="deletefiles", default=False,
        help="Delete files in bucket")
    (options, args) = opt_parser.parse_args()
    delete_value = options.deletefiles
    create_value = options.uploadfilepath
    started = datetime.now()
    print "[%s] Start processing S3 update ..." % started.strftime("%Y-%m-%d, %H:%M:%S")
    uploaded_files = []
    if bool(delete_value):
        result = get_destination_filenames(delete_value)
        print "the result-->", result
        for value in result:
            delete_files(value)
    if bool(create_value):
        # create_dir = get_destination_filenames(create_value)
        # create_dirs(create_dir)
        for (source, target) in get_upload_control_data(create_value):
	    print "the source --->", source
	    print "the target--->", target
	    print "\n"
            uploaded_files.append(upload(source, target))
        if not uploaded_files:
            print("No files uploaded")
        else:
            print "Uploaded %s file(s)" % len(uploaded_files)
        ended = datetime.now()
        elapsed = ended - started
        print "[%s] Finished after %s seconds" % (
              ended.strftime("%Y-%m-%d, %H:%M:%S"),
              round(elapsed.total_seconds(), 2))
        put_log_file()


if __name__ == '__main__':
    main()
