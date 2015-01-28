/************************************************************************/
/*                                                                      */
/*   svm_struct_latent_api.c                                            */
/*                                                                      */
/*   API function definitions for Latent SVM^struct                     */
/*                                                                      */
/*   Author: Chun-Nam Yu                                                */
/*   Date: 17.Dec.08                                                    */
/*                                                                      */
/*   This software is available for non-commercial use only. It must    */
/*   not be modified and distributed without prior permission of the    */
/*   author. The author is not responsible for implications from the    */
/*   use of this software.                                              */
/*                                                                      */
/************************************************************************/

#include <stdio.h>
#include <assert.h>
#include "svm_struct_latent_api_types.h"

#define MAX_INPUT_LINE_LENGTH 10000

SAMPLE read_struct_examples(char *file, STRUCT_LEARN_PARM *sparm) {
/*
  Read input examples {(x_1,y_1),...,(x_n,y_n)} from file.
  The type of pattern x and label y has to follow the definition in 
  svm_struct_latent_api_types.h. Latent variables h can be either
  initialized in this function or by calling init_latent_variables(). 
*/
  SAMPLE sample;
  /* your code here */
  int num_examples,i,label;
  FILE *fp;
  char line[MAX_INPUT_LINE_LENGTH]; 
  char *pchar, *last_pchar;

  fp = fopen(file,"r");
  if (fp==NULL) {
    printf("Cannot open input file %s!\n", file);
	exit(1);
  }
  fgets(line, MAX_INPUT_LINE_LENGTH, fp); //read a line
  num_examples = atoi(line); //first line is the number of egs
  sample.n = num_examples;
  sample.examples = (EXAMPLE*)malloc(sizeof(EXAMPLE)*num_examples);

  for (i=0;(!feof(fp))&&(i<num_examples);i++) {
    fgets(line, MAX_INPUT_LINE_LENGTH, fp);
    pchar = line; //&line[0]

	/* get the true label */
    while ((*pchar)!=':') pchar++; //each tuple was seperated by :
    *pchar = '\0'; // change what the pointer points to, make the line the content before :
    sample.examples[i].y.is_satire = atoi(line);
    pchar++;

	/* observable attrs */

	/* title */
	last_pchar = pchar; // last char is the pointer that points to a string ending as '\0'
    while ((*pchar)!=':') pchar++;
    *pchar = '\0';
    sample.examples[i].x.big_title = atoi(last_pchar);
    pchar++;

	/* freebase_score */
	last_pchar = pchar; // last char is the pointer that points to a string ending as '\0'
    while ((*pchar)!=':') pchar++;
    *pchar = '\0';
    sample.examples[i].x.freebase_threshold = atoi(last_pchar);
    pchar++;

	/* is_profane */
	last_pchar = pchar; // last char is the pointer that points to a string ending as '\0'
    while ((*pchar)!=':') pchar++;
    *pchar = '\0';
    sample.examples[i].x.is_profane = atoi(last_pchar);
    pchar++;
	
	/* is_slang */
	last_pchar = pchar; // last char is the pointer that points to a string ending as '\0'
    while ((*pchar)!=':') pchar++;
    *pchar = '\0';
    sample.examples[i].x.is_slang = atoi(last_pchar);
  }
  
  
  fclose(fp);
  return(sample); 
}

void init_struct_model(SAMPLE sample, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm, LEARN_PARM *lparm, KERNEL_PARM *kparm) {
/*
  Initialize parameters in STRUCTMODEL sm. Set the diminension 
  of the feature space sm->sizePsi. Can also initialize your own
  variables in sm here. 
*/

  
  sm->n = sample.n;
  

  sm->sizePsi = 6; /* replace with appropriate number */

  /* your code here*/

}

void init_latent_variables(SAMPLE *sample, LEARN_PARM *lparm, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Initialize latent variables in the first iteration of training.
  Latent variables are stored at sample.examples[i].h, for 1<=i<=sample.n.
*/

  /* your code here */
  int i;
  //init_gen_rand(lparm->biased_hyperplane); //is this neccessary?
  
  for (i=0;i<sample->n;i++){
	if (sample->examples[i].y.is_satire == -1){
	  sample->examples[i].h.speaker_profile = 1;
	  sample->examples[i].h.quote_professionalism = 1;
	  
	}
	else if(sample->examples[i].y.is_satire == 1){
	  sample->examples[i].h.speaker_profile = 1;
	  sample->examples[i].h.quote_professionalism = -1;
	}
  }
  
}

SVECTOR *psi(PATTERN x, LABEL y, LATENT_VAR h, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Creates the feature vector \Psi(x,y,h) and return a pointer to 
  sparse vector SVECTOR in SVM^light format. The dimension of the 
  feature vector returned has to agree with the dimension in sm->sizePsi. 
*/
  SVECTOR *fvec=NULL;  
  
  /* your code here */
  int feactures[6];
  feactures[0] = x.big_title;
  feactures[1] = x.freebase_threshold;
  feactures[2] = x.is_profane;
  feactures[3] = x.is_slang;
  feactures[4] = h.speaker_profile;
  feactures[5] = h.quote_professionalism;
  
  int l = sm->sizePsi;
  WORD *words;
  words = (WORD*)my_malloc(sizeof(WORD)*(l+1));
  int i;
  for(i=0; i< l;i++){
	words[i].wnum = i;
	words[i].weight = feactures[i];
  }
  fvec = create_svector(words,"",1);


  return(fvec);
}

void classify_struct_example(PATTERN x, LABEL *y, LATENT_VAR *h, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Makes prediction with input pattern x with weight vector in sm->w,
  i.e., computing argmax_{(y,h)} <w,psi(x,y,h)>. 
  Output pair (y,h) are stored at location pointed to by 
  pointers *y and *h. 
*/
  
  /* your code here */  
  double prod;
  prod = sm->w[0]*x.big_title + sm->w[1]*x.freebase_threshold + sm->w[2]*x.is_profane + sm->w[3]*x.is_slang; //product of observable features and their weights
  
  double p_max_score = -1E10;

  int yi, h1, h2, y_best;
  for(yi = -1;yi<=1; yi=yi+2){
	if((prod + sm->w[4] + sm->w[5])*yi > p_max_score){
	  h1 = 1;
	  h2 = 1;
	  p_max_score = (prod + sm->w[4] + sm->w[5])*yi;
	  y_best = yi;
	}
	else if((prod + sm->w[4])*yi > p_max_score){
	  h1 = 1;
	  h2 = 0;
	  p_max_score = (prod + sm->w[4])*yi;
	  y_best = yi;
	}
	else if((prod + sm->w[5])*yi > p_max_score){
	  h1 = 0;
	  h2 = 1;
	  p_max_score = (prod + sm->w[5])*yi;
	  y_best = yi;
	}
	else if((prod)*yi >= p_max_score){
	  h1 = 0;
	  h2 = 0;
	  p_max_score = prod*yi;
	  y_best = yi;
	}
  }
  

  //assign results
  y->is_satire = y_best;
  h->speaker_profile = h1;
  h->quote_professionalism = h2;

}

void find_most_violated_constraint_marginrescaling(PATTERN x, LABEL y, LABEL *ybar, LATENT_VAR *hbar, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Finds the most violated constraint (loss-augmented inference), i.e.,
  computing argmax_{(ybar,hbar)} [<w,psi(x,ybar,hbar)> + loss(y,ybar,hbar)].
  The output (ybar,hbar) are stored at location pointed by 
  pointers *ybar and *hbar. 
*/

  /* your code here */
  double prod;
  prod = sm->w[0]*x.big_title + sm->w[1]*x.freebase_threshold + sm->w[2]*x.is_profane + sm->w[3]*x.is_slang; //product of observable features and their weights
  
  double p_max_score = -1E10;
  
  int yi, h1, h2, y_best;
  for(yi = -1;yi<=1; yi=yi+2){
	if((prod + sm->w[4] + sm->w[5])*yi + (yi != y.is_satire) > p_max_score){
	  h1 = 1;
	  h2 = 1;
	  p_max_score = (prod + sm->w[4] + sm->w[5])*yi;
	  y_best = yi;
	}
	else if((prod + sm->w[4])*yi + (yi != y.is_satire) > p_max_score){
	  h1 = 1;
	  h2 = 0;
	  p_max_score = (prod + sm->w[4])*yi;
	  y_best = yi;
	}
	else if((prod + sm->w[5])*yi + (yi != y.is_satire) > p_max_score){
	  h1 = 0;
	  h2 = 1;
	  p_max_score = (prod + sm->w[5])*yi;
	  y_best = yi;
	}
	else if((prod)*yi + (yi != y.is_satire) >= p_max_score){
	  h1 = 0;
	  h2 = 0;
	  p_max_score = prod*yi;
	  y_best = yi;
	}
  }

  ybar->is_satire = y_best;
  hbar->speaker_profile = h1;
  hbar->quote_professionalism = h2;

}

LATENT_VAR infer_latent_variables(PATTERN x, LABEL y, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Complete the latent variable h for labeled examples, i.e.,
  computing argmax_{h} <w,psi(x,y,h)>. 
*/

  LATENT_VAR h;

  /* your code here */
  double prod;
  prod = sm->w[0]*x.big_title + sm->w[1]*x.freebase_threshold + sm->w[2]*x.is_profane + sm->w[3]*x.is_slang; //product of observable features and their weights
  
  double p_max_score = -1E10;

  int h1, h2;

  if((prod + sm->w[4] + sm->w[5])*y.is_satire > p_max_score){
	h1 = 1;
	h2 = 1;
	p_max_score = (prod + sm->w[4] + sm->w[5])*y.is_satire;
  }
  else if((prod + sm->w[4])*y.is_satire > p_max_score){
	h1 = 1;
	h2 = 0;
	p_max_score = (prod + sm->w[4])*y.is_satire;
  }
  else if((prod + sm->w[5])*y.is_satire > p_max_score){
	h1 = 0;
	h2 = 1;
	p_max_score = (prod + sm->w[5])*y.is_satire;
  }
  else if((prod)*y.is_satire >= p_max_score){
	h1 = 0;
	h2 = 0;
	p_max_score = prod*y.is_satire;
  }

  h.speaker_profile = h1;
  h.quote_professionalism = h2;
  return(h); 
}


double loss(LABEL y, LABEL ybar, LATENT_VAR hbar, STRUCT_LEARN_PARM *sparm) {
/*
  Computes the loss of prediction (ybar,hbar) against the
  correct label y. 
*/
  double ans;
  
  /* your code here */
  if (y.is_satire==ybar.is_satire) {
    return(0);
  } else {
    return(1);
  }

  //return(ans);
}

void write_struct_model(char *file, STRUCTMODEL *sm, STRUCT_LEARN_PARM *sparm) {
/*
  Writes the learned weight vector sm->w to file after training. 
*/

  FILE *modelfl;
  int i;
  
  modelfl = fopen(file,"w");
  if (modelfl==NULL) {
    printf("Cannot open model file %s for output!", file);
	exit(1);
  }
  
  /* write model information */

  for (i=0;i<sm->sizePsi;i++) {
    fprintf(modelfl, "%d:%.16g\n", i, sm->w[i]);
  }
  fclose(modelfl);
 
}

STRUCTMODEL read_struct_model(char *file, STRUCT_LEARN_PARM *sparm) {
/*
  Reads in the learned model parameters from file into STRUCTMODEL sm.
  The input file format has to agree with the format in write_struct_model().
*/
  STRUCTMODEL sm;

  /* your code here */

  FILE *modelfl;
  int sizePsi,i, fnum;
  double fweight;
  char line[1000];
  
  modelfl = fopen(file,"r");
  if (modelfl==NULL) {
    printf("Cannot open model file %s for input!", file);
	exit(1);
  }
  
  sizePsi = 6;
  
  sm.sizePsi = sizePsi;
  sm.w = (double*)malloc((sizePsi+1)*sizeof(double));
  for (i=0;i<sizePsi;i++) {
    sm.w[i] = 0.0;
  }
  /* skip first two lines of comments */
  //fgets(line,1000,modelfl);
  //fgets(line,1000,modelfl);
  
  while (!feof(modelfl)) {
    fscanf(modelfl, "%d:%lf", &fnum, &fweight);
	sm.w[fnum] = fweight;
  }

  fclose(modelfl);

  return(sm);

}

void free_struct_model(STRUCTMODEL sm, STRUCT_LEARN_PARM *sparm) {
/*
  Free any memory malloc'ed in STRUCTMODEL sm after training. 
*/

  /* your code here */
  
  free(sm.w);
}

void free_pattern(PATTERN x) {
/*
  Free any memory malloc'ed when creating pattern x. 
*/

  /* your code here */

}

void free_label(LABEL y) {
/*
  Free any memory malloc'ed when creating label y. 
*/

  /* your code here */

} 

void free_latent_var(LATENT_VAR h) {
/*
  Free any memory malloc'ed when creating latent variable h. 
*/

  /* your code here */

}

void free_struct_sample(SAMPLE s) {
/*
  Free the whole training sample. 
*/
  int i;
  for (i=0;i<s.n;i++) {
    free_pattern(s.examples[i].x);
    free_label(s.examples[i].y);
    free_latent_var(s.examples[i].h);
  }
  free(s.examples);

}

void parse_struct_parameters(STRUCT_LEARN_PARM *sparm) {
/*
  Parse parameters for structured output learning passed 
  via the command line. 
*/
  int i;
  
  /* set default */
  
  for (i=0;(i<sparm->custom_argc)&&((sparm->custom_argv[i])[0]=='-');i++) {
    switch ((sparm->custom_argv[i])[2]) {
      /* your code here */
      default: printf("\nUnrecognized option %s!\n\n", sparm->custom_argv[i]); exit(0);
    }
  }
}

