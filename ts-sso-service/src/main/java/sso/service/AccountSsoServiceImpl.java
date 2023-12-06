package sso.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.stereotype.Service;
import sso.domain.*;
import sso.repository.AccountRepository;
import sso.repository.LoginUserListRepository;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

@Service
public class AccountSsoServiceImpl implements AccountSsoService{

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private StringRedisTemplate template;

//    @Autowired
//    private LoginUserListRepository loginUserListRepository;

    @Override
    public Account createAccount(Account account){

        if(accountRepository.findById(account.getId()) != null){
            System.out.println("[SSO Service][Init Account] Account Already Exists.");
            return account;
        }
        System.out.println("[SSO Service][Init Account] Before:" + account.getId());
        Account resultAcc = accountRepository.save(account);
        Account oldAcc = accountRepository.findByEmail(account.getEmail());
        System.out.println("[SSO Service][Init Account] After:" + oldAcc.getId());
        return resultAcc;
    }

    @Override
    public RegisterResult create(RegisterInfo ri){
        Account oldAcc = accountRepository.findByEmail(ri.getEmail());
        if(oldAcc != null){
            RegisterResult rr = new RegisterResult();
            rr.setStatus(false);
            rr.setMessage("Account Already Exists");
            rr.setAccount(null);
            System.out.println("[SSO Service][Register] Fail.Account already exists.");
            System.out.println("[SSO Service][Register] Register Email:" + ri.getEmail() + " Exist Email:" + oldAcc.getEmail());
            return rr;
        }
        Account account = new Account();
        account.setId(UUID.randomUUID());
        account.setEmail(ri.getEmail());
        account.setPassword(ri.getPassword());
        account.setName(ri.getName());
        account.setDocumentNum(ri.getDocumentNum());
        account.setDocumentType(ri.getDocumentType());
        account.setGender(ri.getGender());
        Account resultAcc = accountRepository.save(account);
        resultAcc.setPassword("");
        System.out.println("[SSO Service][Register] Success.");
        RegisterResult rr = new RegisterResult();
        rr.setStatus(true);
        rr.setMessage("Success");
        rr.setAccount(account);
        return rr;
    }

    @Override
    public LoginResult login(LoginInfo li){
        if(li == null){
            System.out.println("[SSO Service][Login] Fail.Account not found.");
            LoginResult lr = new LoginResult();
            lr.setStatus(false);
            lr.setMessage("Account Not Found");
            lr.setAccount(null);
            return lr;
        }
        Account result = accountRepository.findByEmail(li.getEmail());
        if(result != null &&
                result.getPassword() != null && li.getPassword() != null
                && result.getPassword().equals(li.getPassword())){
            result.setPassword("");
            System.out.println("[SSO Service][Login] Success.");
            LoginResult lr = new LoginResult();
            lr.setStatus(true);
            lr.setMessage("Success");
            lr.setAccount(result);
            return lr;
        }else{
            LoginResult lr = new LoginResult();
            lr.setStatus(false);
            lr.setAccount(null);
            if(result == null){
                lr.setMessage("Account Not Exist");
                System.out.println("[SSO Service][Login] Fail.Account Not Exist.");
            }else{
                lr.setMessage("Password Wrong");
                System.out.println("[SSO Service][Login] Fail.Wrong Password.");
            }
            return lr;
        }
    }

    @Override
    public PutLoginResult loginPutToken(String loginId){
        PutLoginResult plr = new PutLoginResult();
        //if(loginUserList.keySet().contains(loginId)){
        if(this.template.hasKey(loginId)){

            String token = UUID.randomUUID().toString();
            ValueOperations<String, String> ops = this.template.opsForValue();
            ops.set(loginId,token);
            //loginUserList.put(loginId,token);
            System.out.println("[Account-SSO-Service][Login] Login Success. Id:" + loginId + " Token:" + token);
            plr.setStatus(true);
            plr.setLoginId(loginId);
            plr.setMsg("Success.Already Login");
            plr.setToken(token);


//            System.out.println("[Account-SSO-Service][Login] Already Login, Token:" + loginId);
//            plr.setStatus(true);
//            plr.setLoginId(loginId);
//            plr.setMsg("Already Login");
//            plr.setToken(null);

        }else{
            String token = UUID.randomUUID().toString();
            ValueOperations<String, String> ops = this.template.opsForValue();
            ops.set(loginId,token);
            //loginUserList.put(loginId,token);
            System.out.println("[Account-SSO-Service][Login] Login Success. Id:" + loginId + " Token:" + token);
            plr.setStatus(true);
            plr.setLoginId(loginId);
            plr.setMsg("Success");
            plr.setToken(token);
        }
        return plr;
    }

    @Override
    public LogoutResult logoutDeleteToken(LogoutInfo li){
        LogoutResult lr = new LogoutResult();
        if(!this.template.hasKey(li.getId())){
            System.out.println("[Account-SSO-Service][Logout] Already Logout. LogoutId:" + li.getId());
            lr.setStatus(false);
            lr.setMessage("Not Login");
        }else{
            ValueOperations<String, String> ops = this.template.opsForValue();
            String savedToken = ops.get(li.getId());
            if(savedToken.equals(li.getToken())){
                this.template.delete(li.getId());
                lr.setStatus(true);
                lr.setMessage("Success");
            }else{
                lr.setStatus(false);
                lr.setMessage("Token Wrong");
            }
        }
        return lr;
    }

    @Override
    public VerifyResult verifyLoginToken(String verifyToken){
        System.out.println("[Account-SSO-Service][Verify] Verify token:" + verifyToken);
        VerifyResult vr = new VerifyResult();

        boolean exist = isExist(verifyToken);
        if(exist){
            vr.setStatus(true);
            vr.setMessage("Verify Success.");
            System.out.println("[Account-SSO-Service][Verify] Success.Token:" + verifyToken);
        }else{
            vr.setStatus(false);
            vr.setMessage("Verify Fail.");
            System.out.println("[Account-SSO-Service][Verify] Fail.Token:" + verifyToken);
        }
        return vr;
    }

    private boolean isExist(String verifyToken){
        boolean result = false;
        ValueOperations<String, String> ops = this.template.opsForValue();
        Set<String> keys = this.template.keys("*");
        for(String key : keys){
            if(ops.get(key).equals(verifyToken)){
                result = true;
                break;
            }
        }
        return result;
    }

    @Override
    public FindAllAccountResult findAllAccount(){
        FindAllAccountResult findAllAccountResult = new FindAllAccountResult();
        ArrayList<Account> accounts = accountRepository.findAll();
        for(int i = 0;i < accounts.size();i++){
            System.out.println("[SSO Service][Find All Account]" + accounts.get(i).getId());
        }
        findAllAccountResult.setStatus(true);
        findAllAccountResult.setMessage("Success.");
        findAllAccountResult.setAccountArrayList(accounts);
        return findAllAccountResult;
    }

    @Override
    public GetLoginAccountList findAllLoginAccount(){
        ArrayList<LoginAccountValue> values = new ArrayList<>();
        ValueOperations<String, String> ops = this.template.opsForValue();

        Set<String> keys = this.template.keys("*");
        for(String key : keys){
            String token = ops.get(key);
            values.add(new LoginAccountValue(key,token));
        }


        GetLoginAccountList getLoginAccountList = new GetLoginAccountList();
        getLoginAccountList.setStatus(true);
        getLoginAccountList.setMessage("Success");
        getLoginAccountList.setLoginAccountList(values);
        return getLoginAccountList;
    }

    @Override
    public ModifyAccountResult saveChanges(ModifyAccountInfo modifyAccountInfo){
        Account existAccount = accountRepository.findByEmail(modifyAccountInfo.getNewEmail());
        ModifyAccountResult result = new ModifyAccountResult();
        if(existAccount != null && !modifyAccountInfo.getAccountId().equals(existAccount.getId().toString())){
            System.out.println("[SSO Service][Modify Info] Email exists.");
            result.setStatus(false);
            result.setMessage("Email Has Been Occupied.");
            return result;
        }

        System.out.println("[SSO Service][Modify Info] Account Id:" + modifyAccountInfo.getAccountId());
        Account oldAccount = accountRepository.findById(UUID.fromString(modifyAccountInfo.getAccountId()));

        if(oldAccount == null){
            System.out.println("[SSO Service][Modify Info] Fail.Can not found account.");
            result.setStatus(false);
            result.setMessage("Account Not Found.");
        }else{
            oldAccount.setEmail(modifyAccountInfo.getNewEmail());
            oldAccount.setPassword(modifyAccountInfo.getNewPassword());
            oldAccount.setName(modifyAccountInfo.getNewName());
            oldAccount.setGender(modifyAccountInfo.getNewGender());
            oldAccount.setDocumentType(modifyAccountInfo.getNewDocumentType());
            oldAccount.setDocumentNum(modifyAccountInfo.getNewDocumentNumber());
            accountRepository.save(oldAccount);
            //oldAccount.setPassword("");
            System.out.println("[SSO Service][ModifyInfo] Success.");
            result.setStatus(true);
            result.setMessage("Success.");
        }
        return result;
    }

    public GetAccountByIdResult getAccountById(GetAccountByIdInfo info){
        Account account = accountRepository.findById(UUID.fromString(info.getAccountId()));
        GetAccountByIdResult result = new GetAccountByIdResult();
        if(account == null){
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setAccount(null);
        }else{
            result.setStatus(true);
            result.setMessage("Success");
            result.setAccount(account);
        }
        return result;
    }

    @Override
    public Contacts adminLogin(String name, String password) {
        Contacts c = null;
        if("adminroot".equals(name) && "adminroot".equals(password)){
            c = new Contacts();
            c.setId(UUID.fromString("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f"));
            c.setName("adminroot");
            System.out.println("[SSO Service][Admin Login successfully!]");
        }else{
            System.out.println("[SSO Service][Admin Login fail!]");
        }
        return c;
    }

    @Override
    public DeleteAccountResult deleteAccount(String accountId) {
        Account account = accountRepository.findById(UUID.fromString(accountId));
        DeleteAccountResult result = new DeleteAccountResult();
        if(account == null){
            result.setStatus(false);
            result.setMessage("Delete account failed!");
            result.setAccount(null);
        }
        else{
            accountRepository.deleteById(account.getId());
            result.setStatus(true);
            result.setMessage("Delete account successfully!");
            result.setAccount(account);
        }
        return result;
    }
}

