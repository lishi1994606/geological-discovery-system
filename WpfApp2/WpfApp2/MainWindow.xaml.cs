using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using JiebaNet.Segmenter; // 分词
using System.Collections.ObjectModel;  //引入model
using System.IO;
using NPOI.XSSF.UserModel;
using NPOI.HSSF.UserModel;
using NPOI.SS.UserModel;
using System.Runtime.Serialization.Formatters.Binary;
using System.Runtime.Serialization;
using StackExchange.Redis;
using System.Windows.Threading;
using System.Diagnostics;
using WpfApp2;
/*
全球古生物数据库
全球矿产资源相关数据库
 */


namespace WpfApp2
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : System.Windows.Window
    {
        //private List<String> segments;
        private IList<Word> list = new ObservableCollection<Word>() { };
        private IList<Word> listTemp = new List<Word>() { };
        //检索结果集
        private ObservableCollection<SearchResult> listResult = new ObservableCollection<SearchResult>() { };

        public static Window mainWindow = null;
        ////全球古生物数据库
        //private IList<SearchResult> srList1 = new ObservableCollection<SearchResult>() { };
        ////全球矿产资源相关数据库
        //private IList<SearchResult> srList2 = new ObservableCollection<SearchResult>() { };
        
        //定时器
        private  DispatcherTimer showTimerBase = new DispatcherTimer();  //基本参数的定时器
        private DispatcherTimer showTimerContent = new DispatcherTimer(); //所有网址信息的定时器
        private String p = @"F:\博二其他文件\DDE\baidu_google_search\0303_Google\ls_spider\";

        public MainWindow()
        {
            InitializeComponent();
            this.listbox1.ItemsSource = list;
            mainWindow = this;

        }


        private void Timer_Tick(object sender, EventArgs e)
        {
            //showTimer.Tick += new EventHandler(SetNull); 
            //todo
            //获取温度的数值

            //获取年月日
            string dt_ymd = DateTime.Now.ToLongDateString();
            //获取几时几分
            string dt_hm = DateTime.Now.ToShortTimeString();
  

            //获取今天是星期几
            string[] Day = new string[] { "星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六" };
            string week = Day[Convert.ToInt32(DateTime.Now.DayOfWeek.ToString("d"))].ToString();
            MessageBox.Show(week);
        }

        private void timetest(object sender,EventArgs e)
        {
            showTimerBase.Tick += new EventHandler(SetNull);
            showTimerBase.Interval = new TimeSpan(0, 0, 0, 6);
            showTimerBase.Start();  
        }
         private  void SetNull(object sender,EventArgs e)
        {
            this.geshu.Content=DateTime.Now.ToLongDateString();
        }


        public void initResult(double yz)
        {
            double yuzhi = yz;
            DateTime dt = DateTime.Now;
            SearchResult result1 = new SearchResult();
            result1.Url = "http://www.chinapsc.cn";
            result1.Name = "中国古生物学会";
            result1.SearchTime = dt.ToLocalTime().ToString();
            result1.Yuzhi = 2.8;
            if (result1.Yuzhi > yuzhi)
            {
                listResult.Add(result1);
            }
            

            SearchResult result2 = new SearchResult();
            result2.Url = "https://paleobiodb.org/";
            result2.Name = "在线古生物数据库";
            result2.SearchTime = dt.AddSeconds(5).ToLocalTime().ToString();
            result2.Yuzhi = 2.0;
            listResult.Add(result2);
            if (result2.Yuzhi > yuzhi)
            {
                listResult.Add(result2);
            }

            SearchResult result3 = new SearchResult();
            result3.Url = "http://www.uua.cn/";
            result3.Name = "化石网";
            result3.SearchTime = dt.AddSeconds(7).ToLocalTime().ToString();
            result3.Yuzhi = 1.5;
            if (result3.Yuzhi > yuzhi)
            {
                listResult.Add(result3);
            }

            SearchResult result4 = new SearchResult();
            result4.Url = "http://gswxb.cnjournals.cn/ch/index.aspx";
            result4.Name = "古生物学报";
            result4.SearchTime = dt.AddSeconds(8).ToLocalTime().ToString();
            result4.Yuzhi = 1.8;
            if (result4.Yuzhi > yuzhi)
            {
                listResult.Add(result4);
            }

            SearchResult result5 = new SearchResult();
            result5.Url = "http://www.dx.cdut.edu.cn/";
            result5.Name = "地质学国家级实验教学示范中心";
            result5.SearchTime = dt.AddSeconds(10).ToLocalTime().ToString();
            result5.Yuzhi=2.0;
            if (result5.Yuzhi > yuzhi)
            {
                listResult.Add(result5);
            }

            SearchResult result6 = new SearchResult();
            result6.Url = "http://wsgt.cbpt.cnki.net/WKE/WebPublication/index.aspx?mid=WSGT ";
            result6.Name = "微体古生物学报";
            result6.SearchTime = dt.AddSeconds(11).ToLocalTime().ToString();
            result6.Yuzhi=2.4;
            if (result6.Yuzhi > yuzhi)
            {
                listResult.Add(result6);
            }

            SearchResult result7 = new SearchResult();
            result7.Url = "http://www.nigpas.cas.cn/";
            result7.Name = "中国科学院南京古生物地质研究所";
            result7.SearchTime = dt.AddSeconds(12).ToLocalTime().ToString();
            result7.Yuzhi=2.6;
            if (result7.Yuzhi > yuzhi)
            {
                listResult.Add(result7);
            }

            SearchResult result8 = new SearchResult();
            result8.Url = "http://www.irgrid.ac.cn/";
            result8.Name = "中国科学院机构知识库网格";
            result8.SearchTime = dt.AddSeconds(13).ToLocalTime().ToString();
            result8.Yuzhi = 2.3;
            if (result8.Yuzhi > yuzhi)
            {
                listResult.Add(result8);
            }

            SearchResult result9 = new SearchResult();
            result9.Url = "http://www.sklps.cn/";
            result9.Name = "现代古生物学和地层学国家重点实验室";
            result9.SearchTime = dt.AddSeconds(15).ToLocalTime().ToString();
            result9.Yuzhi = 2.7;
            if (result9.Yuzhi > yuzhi)
            {
                listResult.Add(result9);
            }

            SearchResult result10 = new SearchResult();
            result10.Url = "http://www.iue.cas.cn/jgsz/kyjg/csstjkyhjaqyjzx/cstryswhx/";
            result10.Name = "中国科学院城市环境研究所";
            result10.SearchTime = dt.AddSeconds(20).ToLocalTime().ToString();
            result10.Yuzhi = 2.2;
            if (result10.Yuzhi > yuzhi)
            {
                listResult.Add(result10);
            }

        }

        public static String Num1;

        #region
        //分词
        #endregion
        //分词
        private void bc1(Object sender,RoutedEventArgs e) 
        {
            Num1 = "20000";

            //MessageBox.Show(e.ToString());
            //1.初始化
            var segmenter = new JiebaSegmenter();
            segmenter.LoadUserDict("C:\\jieba\\config\\lishi_dict.txt"); //添加专用词典
            //list  清空
            list.Clear();
            listTemp.Clear();

            //2.读取输入并分词
            String text = box1.Text;
            //var conn = ConnectionMultiplexer.Connect("localhost");
            //IDatabase db = conn.GetDatabase();
            //db.KeyDelete("guanjianci");
            //db.StringSet("guanjianci",text);
            //conn.Close();

            var segments= segmenter.Cut(text);
            //MessageBox.Show("分词为："+ string.Join("/ ", segments));
            //list.Add(string.Join("/ ", segments));
            foreach(Object obj in segments)
            {
                if (" ".Equals((string)obj)) {  //去掉空格
                    continue;
                }
               if(obj is String)
               {
                    Word word = new Word();
                    word.Words = (String)obj;
                    word.Flag = "PT";
                
                   foreach(Word w in list){
                       if (w.Words == word.Words) {
                           continue;
                       }
                   }
                   

                   listTemp.Add(word);
                    list.Add(word);
                }
            }
      
            //this.listbox1.ItemsSource = list;

            //Console.WriteLine("【精确】：{0}", string.Join("/ ", segments));


            //var segments = segmenter.Cut("全球古生物数据库");
            //Console.WriteLine("【精确】：{0}", string.Join("/ ", segments));
            //var segments1 = segmenter.Cut("全球矿产资源相关数据库");
            //Console.WriteLine("【精确】：{0}", string.Join("/ ", segments1));
        }

        #region
        //地址叙词表比对
        #endregion
        private void bc2(Object sender, RoutedEventArgs e)
        {
            if (list.Count == 0)
            {
                MessageBox.Show("请先分词");
            }

            list.Clear();
            //删除keyword_list和keyword_list_value
            var conn = ConnectionMultiplexer.Connect("localhost");
            IDatabase db = conn.GetDatabase();
            db.KeyDelete("keyword_list");
            db.KeyDelete("keyword_list_value");

            foreach (Word w1 in listTemp)
            {
                list.Add(w1);
            }

            string excelPath = "F:\\博二其他文件\\DDE\\baidu_google_search\\0303_Google\\地质汉语叙词表（+沉积学英文）.xls";
            IWorkbook wk = null;
            string extension = System.IO.Path.GetExtension(excelPath);
            //深复制list，避免因在查找过程中list产生变化而导致的问题
            

            try
            {
                FileStream fs = File.OpenRead(excelPath);
                if (extension.Equals(".xls"))
                {
                    wk = new HSSFWorkbook(fs);
                }
                else
                {
                    wk = new XSSFWorkbook(fs);
                }
                fs.Close();

                ISheet sheet = wk.GetSheetAt(0);



                foreach (Word w in listTemp)
                {

                    searchExcel(w,sheet);

                }
            }
            catch(Exception ea) 
            {
                Console.Write(ea.Message);
                MessageBox.Show(ea.Message);
            }


        }

        //执行
        public void bc3(Object sender, RoutedEventArgs e)
        {
            if (this.cengji.Text == "输入爬取层级数")
            {
                MessageBox.Show(Application.Current.MainWindow,"请输入层级");
            }
            if (this.yuzhi1.Text == "" || this.yuzhi2.Text=="" || this.yuzhi3.Text=="")
            {
                MessageBox.Show("请输入阈值");
            }
            
            try
            {
                double yz1 = Convert.ToDouble(this.yuzhi1.Text);
                double yz2 = Convert.ToDouble(this.yuzhi2.Text);
                double yz3 = Convert.ToDouble(this.yuzhi3.Text);

                
                var conn = ConnectionMultiplexer.Connect("localhost");
                IDatabase db = conn.GetDatabase();
                db.StringSet("yuzhi1", this.yuzhi1.Text);
                db.StringSet("yuzhi2", this.yuzhi2.Text);
                db.StringSet("yuzhi3", this.yuzhi3.Text);
                conn.Close();
            }
            catch (Exception ee)
            {
                MessageBox.Show("阈值输入有误，请重新输入");
                return;
            }

            listResult.Clear();
            //initResult(yz);
            this.listView.ItemsSource = listResult;

            //基本信息定时启动
            showTimerBase.Tick += new EventHandler(readFromRedis);
            showTimerBase.Interval = new TimeSpan(0, 0, 0, 3);
            showTimerBase.Start();
            //网址信息定时启动
            showTimerContent.Tick += new EventHandler(readAllUrlContent);
            showTimerContent.Interval = new TimeSpan(0, 0, 0, 5);
            showTimerContent.Start();

            //将搜索词写入redis，
            var conn1 = ConnectionMultiplexer.Connect("localhost");
            IDatabase db1 = conn1.GetDatabase();
            db1.KeyDelete("guanjianci");
            db1.StringSet("guanjianci", this.box1.Text);
            conn1.Close();

            MessageBox.Show("初始化开始！");
            runBat(p,"run.bat");
            MessageBox.Show("初始化结束");
        }

        //下载
        private void bc4(Object sender, RoutedEventArgs e)
        {

            if (list.Count == 0)
            {
                MessageBox.Show("请先分词和查找叙词表");
            }

            Microsoft.Win32.SaveFileDialog dlg = new Microsoft.Win32.SaveFileDialog();

            //将serarchresult 中的结果转换成一个字符串
            //String s_result = "";
            //foreach (SearchResult s in listResult)
            //{
            //    s_result = s_result + String.Format("{0}\t\t\t\t\t\t\t{1}\t\t\t\t\t{2}\r\n", s.Name,s.Url,s.SearchTime);
            //}

            //设置默认文件类型
            //dlg.DefaultExt = ".txt";
            //Nullable<bool> result = dlg.ShowDialog();

            //if (result == true)
            //{
            //    //获取要保存文件名的完整路径
            //    string filename = dlg.FileName;
            //    //将文件流写入文件
            //    FileStream write = new FileStream(filename, FileMode.OpenOrCreate, FileAccess.ReadWrite, System.IO.FileShare.Read);
            //    byte[] data = System.Text.Encoding.Default.GetBytes(s_result);
            //    write.Write(data, 0, data.Length);
            //    write.Close();
            //    MessageBox.Show("成功保存");
            //}

            //设置默认文件类型
            dlg.DefaultExt = ".zip";
            Nullable<bool> result = dlg.ShowDialog();

            //从redis中读取文件的目录
            var conn = ConnectionMultiplexer.Connect("localhost");
            IDatabase db = conn.GetDatabase();
            string path = db.StringGet("result_path");
            conn.Close();

            //将这个result文件压缩后再保存
            ZipHelper.CreateZip(path, path + ".zip");
            //开始读写文件并保存
            if (result == true)
            {
                //获取要保存文件名的完整路径
                string filename = dlg.FileName;
                //将文件流写入文件
                FileStream write = new FileStream(filename, FileMode.OpenOrCreate, FileAccess.ReadWrite, System.IO.FileShare.Read);

                FileStream fs = new FileStream(path+".zip", FileMode.Open);
                //把文件读取到字节数组
                byte[] data = new byte[fs.Length];
                fs.Read(data, 0, data.Length);
                fs.Close();

                write.Write(data, 0, data.Length);
                write.Close();
                MessageBox.Show("成功保存");
            }

        }


        private void bc001(Object sender, RoutedEventArgs e) {

            runBat(p, "run1.bat");
            MessageBox.Show("第一级爬取完成");
        }

        private void bc002(Object sender, RoutedEventArgs e)
        {
            runBat(p, "run2.bat");
            MessageBox.Show("第二级爬取完成");
        }
        private void bc003(Object sender, RoutedEventArgs e)
        {
            runBat(p, "run3.bat");
            MessageBox.Show("第三级爬取完成");
        }

        //excel中查找相关词
        public void searchExcel(Word w,ISheet sheet)
        {
            int nums = sheet.LastRowNum;
            IList<Word> ll = new List<Word>();
            IList<String> temp = new List<String>();
            IList<String> keyword_list = new List<String>(); // 相关词 写入redis提供给python
            IList<Double> keyword_list_value = new List<Double>(); // 相关词的值 写入redis提供给python
            int flag = 0;
            string sss = "";

            //把之前的删掉
            var conn = ConnectionMultiplexer.Connect("localhost");
            IDatabase db = conn.GetDatabase();
            db.KeyDelete("keyword_list");
            db.KeyDelete("keyword_list_value");


            for (int i = 2; i < nums; i++)
            {
                ICell cell = sheet.GetRow(i).GetCell(7);
                ICell cell_BT = sheet.GetRow(i).GetCell(2);
                ICell cell_RT = sheet.GetRow(i).GetCell(4);
                ICell cell_NT = sheet.GetRow(i).GetCell(1);
                ICell cell_TT = sheet.GetRow(i).GetCell(3);
                if (cell != null && cell.CellType != CellType.Blank && cell.ToString().Contains(w.Words))
                {
                    flag = 0;
                    if (cell_BT != null && cell_BT.CellType != CellType.Blank)
                    {
                        String temp_BT = cell_BT.ToString();
                        temp = getWord(temp_BT);
                        foreach (String s in temp)
                        {
                            Word word = new Word();
                            word.Words = s;
                            word.Flag = "BT";
                            list.Add(word);
                        }
                        flag++;
                    }
                    if (cell_RT != null && cell_RT.CellType != CellType.Blank)
                    {
                        String temp_RT = cell_RT.ToString();
                        temp = getWord(temp_RT);
                        foreach (String s in temp)
                        {
                            Word word = new Word();
                            word.Words = s;
                            word.Flag = "RT";
                            list.Add(word);
                        }
                        flag++;
                    }
                    if (cell_NT != null && cell_NT.CellType != CellType.Blank)
                    {
                        String temp_RT = cell_NT.ToString();
                        temp = getWord(temp_RT);
                        foreach (String s in temp)
                        {
                            Word word = new Word();
                            word.Words = s;
                            word.Flag = "NT";
                            list.Add(word);
                        }
                        flag++;
                    }
                    if (cell_TT != null && cell_TT.CellType != CellType.Blank)
                    {
                        String temp_RT = cell_TT.ToString();
                        temp = getWord(temp_RT);
                        foreach (String s in temp)
                        {
                            Word word = new Word();
                            word.Words = s;
                            word.Flag = "TT";
                            list.Add(word);
                        }
                        flag++;
                    }
                }
            }
            if (flag == 0)
            {
                list.Remove(w);
            }

            //去重
            try
            {
                foreach (Word ww3 in list)
                {
                    int i = 0;
                    foreach (Word ww4 in list)
                    {
                        if (ww3.Words == ww4.Words)
                        {
                            i = i + 1;
                            if (i > 1)
                            {
                                list.Remove(ww4);
                            }
                        }
                    }
                }
            }catch(Exception){
                Console.WriteLine("禁止这个提示：集合已修改；可能无法执行枚举操作");
            }

            foreach(Word d in list)
            {
                sss = sss +"'"+ d.Words + "', ";
                keyword_list.Add(d.Words);
                if (d.Flag == "PT") 
                {
                    keyword_list_value.Add(1.0);
                }
                else if (d.Flag == "BT")
                {
                    keyword_list_value.Add(0.5);
                }
                else if (d.Flag == "RT")
                {
                    keyword_list_value.Add(0.8);
                }
                else if (d.Flag == "NT")
                {
                    keyword_list_value.Add(0.8);
                }
                else if (d.Flag == "TT")
                {
                    keyword_list_value.Add(0.5);
                }

            }
            System.Console.Write(sss);



            //循环写入redis提供给python
            foreach(String k1 in keyword_list)
            {
                db.ListRightPush("keyword_list", k1);
            }
            foreach (Double k2 in keyword_list_value)
            {
                db.ListRightPush("keyword_list_value", k2);
            }
            conn.Close();

        }

        public List<String> getWord(String str)
        {
            List<String> result = new List<String>();
            if (str.Contains(','))
            {
                result = str.Split(',').ToList();
            }
            else
            {
                result.Add(str);
            }
            return result;
        }

        //读取redis中的一级二级三级连接的数目一级解析完成的数目
        private void readFromRedis(object sender,EventArgs e)
        {
            var conn = ConnectionMultiplexer.Connect("localhost");
            IDatabase db = conn.GetDatabase();

            try
            {
                //一级链接数
                int num_1 = int.Parse(db.StringGet("num_1"));
                this.num1.Text = num_1.ToString();
                int num_2 = int.Parse(db.StringGet("num_2"));
                this.num2.Text = num_2.ToString();
                int num_3 = int.Parse(db.StringGet("num_3"));
                this.num3.Text = num_3.ToString();

                //总链接数
                int num_total = num_1 + num_2 + num_3;
                this.numTotal.Text = num_total.ToString();

                //解析的链接数
                //long num_complete = db.SetLength("result*");
                long num_complete = long.Parse(db.StringGet("parse_num_1")) + long.Parse(db.StringGet("parse_num_2")) + long.Parse(db.StringGet("parse_num_3"));

                this.numComplete.Text = num_complete.ToString();
            }
            catch 
            {
                System.Console.Write("没有数据，继续等待");
            }
            //运行状态设置
            this.runStatus.Text = "运行正常";

            conn.Close();
        }

        //读取redis中所有的网址
        public void readAllUrlContent(object sender, EventArgs e)
        {
            var conn = ConnectionMultiplexer.Connect("localhost");
            IDatabase db = conn.GetDatabase();
            int i = 0;
            RedisValue[] result = new RedisValue[6];
            //var urlList = new RedisValue[100];
            //读取网址
             var urlList = db.SetMembers("urllist1");
            listResult.Clear();
            foreach (RedisValue v in urlList)
            {
                i++;
                if (i > 100)
                {
                    listResult.RemoveAt(0);
                    //break;
                }
                System.Console.WriteLine((String)v);
                if(db.HashExists("result1:"+(string)v,"name"))
                {
                    result = db.HashGet("result1:" + (string)v, new RedisValue[] { "name", "url", "cj", "cc", "tt", "searchTime" });
                }
                SearchResult resultone = new SearchResult();
                resultone.Url = (string)result[1];
                resultone.Name = (string)result[0];
                resultone.SearchTime = (string)result[5];
                resultone.Cc = (string)result[3];
                resultone.Cj = (string)result[2];
                resultone.Tt = (string)result[4];
                listResult.Add(resultone);
            }
            this.geshu.Content = urlList.GetLength(0).ToString();
            conn.Close();
        }
        //刷新
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            //readFromRedis();
            
        }
        
        //调用bat文件
        public void runBat(String path,String name){

            Process proc = new Process();
            string targetDir = string.Format(path);

            proc.StartInfo.WorkingDirectory = targetDir;
            proc.StartInfo.FileName = name;
            proc.StartInfo.Arguments = string.Format("10");

            proc.Start();
            proc.WaitForExit();
        }
    
    }

    public class Word
    {
        private String words;

        public String Words
        {
            get { return words; }
            set { words = value; }
        }
        private String flag;

        public String Flag
        {
            get { return flag; }
            set { flag = value; }
        }
    }


    public class SearchResult
    {
        private String name;
        private String url;
        private String content;
        private String searchTime;
        private String cc;
        private String cj;
        private String tt;
        private double yuzhi;

        public String Cc
        {
          get { return cc; }
          set { cc = value; }
        }
        

        public String Cj
        {
          get { return cj; }
          set { cj = value; }
        }
        

        public String Tt
        {
          get { return tt; }
          set { tt = value; }
        }

        public double Yuzhi
        {
            get { return yuzhi; }
            set { yuzhi = value; }
        }

        public String Name
        {
            get { return name; }
            set { name = value; }
        }

        public String Url
        {
            get { return url; }
            set { url = value; }
        }

        public String Content
        {
            get { return content; }
            set { content = value; }
        }
        public String SearchTime
        {
            get { return searchTime; }
            set { searchTime = value; }
        }

    }




}
