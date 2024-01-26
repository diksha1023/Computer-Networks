#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>


/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */


int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* port = argv[2];

  int s;
  struct addrinfo hints, *result, *rp;
 
  
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_UNSPEC; 
  hints.ai_socktype = SOCK_STREAM; 
  hints.ai_flags = AI_PASSIVE;  
  hints.ai_protocol = IPPROTO_TCP; 
  
  /*
    STUDENT CODE HERE
   */

  s = getaddrinfo(host, port, &hints, &result);
  if (s != 0) {
	  fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
	  exit(EXIT_FAILURE);
  }

 
  for (rp = result; rp != NULL; rp = rp->ai_next) {
	  void* raw_addr;
	  char op[128];

	  if (rp->ai_family == AF_INET) {
	    struct sockaddr_in* tmp = (struct sockaddr_in*)rp->ai_addr;
	      raw_addr = &(tmp->sin_addr);
	      inet_ntop(rp->ai_family, raw_addr, op, sizeof(op));
	      printf("Ouput IPv4: %s \n",op);

  }
	  else { 
	    struct sockaddr_in6* tmp = (struct sockaddr_in6*)rp->ai_addr;
	      raw_addr = &(tmp->sin6_addr); 
	      inet_ntop(rp->ai_family, raw_addr, op, sizeof(op));
	      printf("Output IPv6 %s \n",op);
	  }
  }

  return 0;
}
