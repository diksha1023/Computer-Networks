#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);

/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];

  /* 
     STUDENT CODE HERE
   */

  printf("rcpt: %s\n",rcpt);
  printf("filepath: %s\n",filepath);
  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  printf("Socket : %d\n",socket);
  FILE *ptr= fopen(filepath,"r");

  char response[4096];

  if(NULL==ptr){
	  send_smtp(socket,"",response,0);
  }

  char msg[4096];
  char s[4096];
  while(fgets(s,4096,ptr)!=NULL) {
	  strcat(msg,s);
	 // printf("msg %s\n",msg);		          
  }
  
  fclose(ptr);

  //printf("Msg %s\n",msg);
  //printf("Size %zu\n",strlen(msg));
  
  send_smtp(socket, "HELO iu.edu\n",response,4096);
  printf("Response%s\n",response);
  
  char temp_msg[4096];
  
  sprintf(temp_msg, "%s%s%s\n","MAIL FROM:<",rcpt,">");
  
  send_smtp(socket,temp_msg,response,4096);
  printf("%s\n",response);
  
  sprintf(temp_msg,"%s%s%s\n", "RCPT TO:<",rcpt,">");
  send_smtp(socket,temp_msg,response,4096);
  printf("%s\n",response);
  
  send_smtp(socket,"DATA\n", response, 4096);
  printf("%s\n",response);
  
  strcat(msg,"\r\n.\r\n");
  
  send_smtp(socket, msg,response, 4096);
  printf("%s\n",response);

  return 0;
}
