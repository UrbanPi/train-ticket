import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

/**
 * Created by ZDH on 2017/7/19.
 */
public class TestFlowSuccess {

    private WebDriver driver;
    private String baseUrl;
    private List<WebElement> myOrdersList;

    public static void login(WebDriver driver,String username,String password){
        driver.findElement(By.id("flow_one_page")).click();
        driver.findElement(By.id("flow_preserve_login_email")).clear();
        driver.findElement(By.id("flow_preserve_login_email")).sendKeys(username);
        driver.findElement(By.id("flow_preserve_login_password")).clear();
        driver.findElement(By.id("flow_preserve_login_password")).sendKeys(password);

        try{
            Thread.sleep(new Random().nextInt(6000));
        }catch(Exception e){

        }
        driver.findElement(By.id("flow_preserve_login_button")).click();
    }
    public static String getRandomString(int length) {
        String KeyString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        StringBuffer sb = new StringBuffer();
        int len = KeyString.length();
        for (int i = 0; i < length; i++) {
            sb.append(KeyString.charAt((int) Math.round(Math.random() * (len - 1))));
        }
        return sb.toString();
    }
    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "D:/Program/chromedriver_win32/chromedriver.exe");
        driver = new ChromeDriver();
        baseUrl = "http://10.141.212.22/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    public void testInputSomethingAdmin()throws Exception{

        driver.get(baseUrl + "/");

        driver.findElement(By.id("adminlogin")).click();

        String username = "adminroot";
        String password = "adminroot";

        driver.findElement(By.id("doc-ipt-email-1")).clear();
        driver.findElement(By.id("doc-ipt-email-1")).sendKeys(username);
        driver.findElement(By.id("doc-ipt-pwd-1")).clear();
        driver.findElement(By.id("doc-ipt-pwd-1")).sendKeys(password);

        Thread.sleep(new Random().nextInt(6000));
        driver.findElement(By.id("jcadmin_jclogin_btn")).click();

        Thread.sleep(5000);

        boolean status = new Random().nextBoolean();

        String[] citys = {"beijing", "shanghaihongqiao", "taiyuan", "xuzhou", "jinan", "hangzhou"};
        String fromId = citys[new Random().nextInt(6)];
        String toId = citys[new Random().nextInt(6)];
        if(status == false){
            driver.findElement(By.id("order_search_by_station_from")).clear();
            driver.findElement(By.id("order_search_by_station_from")).sendKeys(fromId);
            driver.findElement(By.id("order_search_by_station_to")).clear();
            driver.findElement(By.id("order_search_by_station_to")).sendKeys(toId);
            Thread.sleep(new Random().nextInt(6000));
            driver.findElement(By.id("order_search_by_station_search_lock")).click();
        }else{
            //Skip
        }

        Thread.sleep(3000);

        Alert javascriptConfirm = driver.switchTo().alert();
        javascriptConfirm.accept();

    }
    @Test(dependsOnMethods = {"testInputSomethingAdmin"})
    public void testLogin()throws Exception{
        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(3000);

        //get login status
        String statusLogin = driver.findElement(By.id("flow_preserve_login_msg")).getText();
        if("".equals(statusLogin))
            System.out.println("Failed to Login! Status is Null!");
        else if(statusLogin.startsWith("Success"))
            System.out.println("Success to Login! Status:"+statusLogin);
        else
            System.out.println("Failed to Login! Status:"+statusLogin);
        Assert.assertEquals(statusLogin.startsWith("Success"),true);
    }

    @Test (dependsOnMethods = {"testLogin"})
    public void testViewAllOrdersThread() throws Exception{

        String js = "document.getElementById('flow_two_page').scrollIntoView(false)";
        ((JavascriptExecutor)driver).executeScript(js);
        driver.findElement(By.id("flow_two_page")).click();


        String js2 = "document.getElementById('refresh_all_order_list_async_button').scrollIntoView(false)";
        ((JavascriptExecutor)driver).executeScript(js2);
        Thread.sleep(new Random().nextInt(6000));
        driver.findElement(By.id("refresh_all_order_list_async_button")).click();

        Thread.sleep(1000);

    }

    @Test (dependsOnMethods = {"testViewAllOrdersThread"})
    public void testViewOrders() throws Exception{
        Thread.sleep(new Random().nextInt(6000));
        driver.findElement(By.id("refresh_my_order_list_button")).click();
        Thread.sleep(1000);
        //gain my oeders
        myOrdersList = driver.findElements(By.xpath("//div[@id='my_orders_result']/div"));
        if (myOrdersList.size() > 0) {
            System.out.printf("Success to show my orders list，the list size is:%d%n",myOrdersList.size());
        } else {
            System.out.println("Failed to show my orders list，the list size is 0 or No orders in this user!");
        }
        Assert.assertEquals(myOrdersList.size() > 0,true);
    }
    @Test (dependsOnMethods = {"testViewOrders"})
    public void testClickOrderCancel() throws Exception{
        System.out.printf("The orders list size is:%d%n",myOrdersList.size());
        String statusOrder  = "";
        int i;
        //Find the first not paid order .
        for(i = 0;i < myOrdersList.size();i++) {
            //while(!(statusOrder.startsWith("Not")) && i < myOrdersList.size()) {
            //statusOrder = myOrdersList.get(i).findElement(By.xpath("/div[2]/div/div/form/div[7]/div/label[2]")).getText();
            statusOrder = myOrdersList.get(i).findElement(By.xpath("div[2]//form[@role='form']/div[7]/div/label[2]")).getText();
            if(statusOrder.startsWith("Paid"))
                break;
        }
        if(i == myOrdersList.size() || i > myOrdersList.size())
            System.out.printf("Failed,there is no not paid order!");
        Assert.assertEquals(i < myOrdersList.size(),true);

        Thread.sleep(1000);
        String js = "document.getElementsByClassName('ticket_cancel_btn')[0].scrollIntoView(false)";
        ((JavascriptExecutor)driver).executeScript(js);
        Thread.sleep(1000);

        Thread.sleep(new Random().nextInt(6000));
        myOrdersList.get(i).findElement(
                By.xpath("div[2]//form[@role='form']/div[12]/div/button[@class='ticket_cancel_btn btn btn-primary']")
        ).click();
        Thread.sleep(500);

        Thread.sleep(new Random().nextInt(6000));
        driver.findElement(By.id("ticket_cancel_panel_confirm")).click();

        Thread.sleep(10000);

        Alert javascriptConfirm = driver.switchTo().alert();
        String statusAlert = driver.switchTo().alert().getText();
        System.out.println("The Alert information of Cancel Ticket："+statusAlert);
        Assert.assertEquals(statusAlert.startsWith("Success"),true);
        javascriptConfirm.accept();
    }


    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
