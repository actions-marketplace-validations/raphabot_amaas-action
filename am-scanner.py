import argparse
import time
import json

import amaas.grpc

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filename', action='store', nargs='*',
                        required=True, help='list of files to be scanned')
    parser.add_argument('-a', '--addr', action='store', default='127.0.0.1:50051', required=False,
                        help='gRPC server address and port (default 127.0.0.1:50051)')
    parser.add_argument('-r', '--region', action='store',
                        help='AMaaS service region; e.g. us-1 or dev')
    parser.add_argument('--api_key', action='store',
                        help='api key for authentication')
    parser.add_argument('--tls', type=bool, action='store', default=True,
                        help='enable TLS gRPC ')
    parser.add_argument('--ca_cert', action='store', help='CA certificate')

    args = parser.parse_args()

    if args.region:
        handle = amaas.grpc.init_by_region(args.region, args.api_key, args.tls, args.ca_cert)
    else:
        handle = amaas.grpc.init(args.addr, args.api_key, args.tls, args.ca_cert)  


    total_result = []
    for file in args.filename:
        s = time.perf_counter()
        result = amaas.grpc.scan_file(file, handle)
        elapsed = time.perf_counter() - s
        result = json.loads(result)
        result['scanDuration'] = f"{elapsed:0.2f}s"
        total_result.append(result)

    print(json.dumps(total_result, indent=1))
    amaas.grpc.quit(handle)