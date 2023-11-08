import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class TestFlowFail {
    private WebDriver driver;
    private String baseUrl;

    public static void login(WebDriver driver,String username,String password){

        //Add random delay to emulate the waiting between user click
        try{
            Thread.sleep(new Random().nextInt(7000) + 3000);
        }catch(Exception e){
            e.printStackTrace();
        }
        driver.findElement(By.id("flow_four_page")).click();
        driver.findElement(By.id("flow_advance_reserve_login_email")).clear();
        driver.findElement(By.id("flow_advance_reserve_login_email")).sendKeys(username);
        driver.findElement(By.id("flow_advance_reserve_login_password")).clear();
        driver.findElement(By.id("flow_advance_reserve_login_password")).sendKeys(password);
        driver.findElement(By.id("flow_advance_reserve_login_button")).click();
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
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    public void testOccupy() throws Exception{
        baseUrl = "http://10.141.212.22:15345/click/occupy";
//        driver.get(baseUrl);
        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(1000);

        //locate booking startingPlace input
        WebElement elementBookingStartingPlace = driver.findElement(By.id("flow_advance_reserve_startingPlace"));
        elementBookingStartingPlace.clear();
        elementBookingStartingPlace.sendKeys("Shang Hai");

        //locate booking terminalPlace input
        WebElement elementBookingTerminalPlace = driver.findElement(By.id("flow_advance_reserve_terminalPlace"));
        elementBookingTerminalPlace.clear();
        elementBookingTerminalPlace.sendKeys("Nan Jing");

        //locate booking Date input
        String bookDate = "";
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
        Calendar newDate = Calendar.getInstance();
        Random randDate = new Random();
        int randomDate = randDate.nextInt(26);
        newDate.add(Calendar.DATE, randomDate+5);
        bookDate=sdf.format(newDate.getTime());

        JavascriptExecutor js = (JavascriptExecutor) driver;
        js.executeScript("document.getElementById('flow_advance_reserve_booking_date').value='"+bookDate+"'");

        //locate Train Type input
        WebElement elementBookingSearchType = driver.findElement(By.id("flow_advance_reserve_select_searchType"));
        Select selTraintype = new Select(elementBookingSearchType);
        selTraintype.selectByValue("1"); //ALL

        //locate Train search button
        WebElement elementBookingSearchBtn = driver.findElement(By.id("flow_advance_reserve_booking_button"));

        for(int i = 0;i < 6;i++){
            Thread.sleep(500);
            elementBookingSearchBtn.click();
        }

    }

    @Test(dependsOnMethods = {"testOccupy"})
    //Test Flow Preserve Step 1: - Login
    public void testLogin()throws Exception{

        baseUrl = "http://10.141.212.21";
        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(1000);
    }

    @Test (dependsOnMethods = {"testLogin"})
    //test Flow Preserve Step 2: - Ticket Booking
    public void testBooking() throws Exception{
        //locate booking startingPlace input
        WebElement elementBookingStartingPlace = driver.findElement(By.id("flow_advance_reserve_startingPlace"));
        elementBookingStartingPlace.clear();
        elementBookingStartingPlace.sendKeys("Shang Hai");

        //locate booking terminalPlace input
        WebElement elementBookingTerminalPlace = driver.findElement(By.id("flow_advance_reserve_terminalPlace"));
        elementBookingTerminalPlace.clear();
        elementBookingTerminalPlace.sendKeys("Nan Jing");

        //locate booking Date input
        String bookDate = "";
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
        Calendar newDate = Calendar.getInstance();
        Random randDate = new Random();
        int randomDate = randDate.nextInt(26);
        newDate.add(Calendar.DATE, randomDate+5);
        bookDate=sdf.format(newDate.getTime());

        JavascriptExecutor js = (JavascriptExecutor) driver;
        js.executeScript("document.getElementById('flow_advance_reserve_booking_date').value='"+bookDate+"'");

        //locate Train Type input
        WebElement elementBookingSearchType = driver.findElement(By.id("flow_advance_reserve_select_searchType"));
        Select selTraintype = new Select(elementBookingSearchType);
        selTraintype.selectByValue("1"); //ALL

        //locate Train search button
        WebElement elementBookingSearchBtn = driver.findElement(By.id("flow_advance_reserve_booking_button"));


        //Add random delay to emulate the waiting between user click
        Thread.sleep(new Random().nextInt(7000) + 3000);
        elementBookingSearchBtn.click();

        Thread.sleep(new Random().nextInt(7000) + 3000);
        elementBookingSearchBtn.click();

    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
