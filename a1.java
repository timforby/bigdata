
import java.io.IOException;
import java.util.Arrays;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class a1 {
  public static class PairingMapper extends Mapper<Object, Text, IntWritable, IntWritable>{
    private static IntWritable a = new IntWritable();
    private static IntWritable b = new IntWritable();
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
      System.out.println(value.toString());
      String[] values = value.toString().split("\\s");
      for(int i = 1 ; i < values.length; i++){
        for(int j = i+1; j < values.length; j++){
          a.set(Integer.parseInt(values[i]));
          b.set(Integer.parseInt(values[j]));
          context.write(a, b);
          context.write(b, a);
        }
      }
    }
  }
  public static class IndexMapper extends Mapper<Object, Text, IntWritable, IntWritable>{
    private static IntWritable a = new IntWritable();
    private static IntWritable b = new IntWritable();
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
      System.out.println(value.toString());
      String[] values = value.toString().split("\\s");
      b.set(Integer.parseInt(values[0]));
      for(int i = 1; i < values.length; i++){

        a.set(Integer.parseInt(values[i]));
        context.write(a, b);
      }
    }
  }
  public static class IndexReducer extends Reducer<IntWritable, IntWritable, IntWritable, Text>{
    private static Text data = new Text();
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
      String list = new String(key.get()+": ");
      for (IntWritable val: values){
        list += val.get();
      }
      data.set(list);
      context.write(key, data);
    }
  }

  public static class PairingReducer extends Reducer<IntWritable, IntWritable, IntWritable, Text>{
    private static Text data = new Text();
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
      int[] nCommons = new int[]{0,0,0,0,0} ;
      for (IntWritable val: values){
        nCommons[val.get()-1]++;
      }
      String list = new String(key.get()+": ");
      for (int i = 0; i < nCommons.length; i++){
        if(nCommons[i]!=0)list += "("+(i+1)+","+nCommons[i]+")";
      }
      data.set(list);
      context.write(key, data);
    }
  }
  public static void main(String[] args) throws Exception{
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "lab2");
    job.setJarByClass(a1.class);
    job.setMapperClass(IndexMapper.class);
    job.setReducerClass(IndexReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0: 1);
  }
}
